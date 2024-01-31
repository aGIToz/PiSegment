import numpy as np
from pyinpaint.utils import *
from PIL import Image
from scipy import spatial
import heapq
from time import time
from collections import defaultdict
import matplotlib.pyplot as plt


def distance_map(edge_index, edge_attr, seed_mask, label):
    num_nodes = len(seed_mask)
    distance_map = np.full(num_nodes, np.inf)
    distance_map[seed_mask] = 0.0
    visited = defaultdict(int)
    s = np.full(num_nodes, np.inf)
    s[seed_mask] = 0.0

    # Initialize the priority queue with seed nodes
    priority_queue = [(0.0, seed) for seed in np.where(seed_mask)[0]]
    heapq.heapify(priority_queue)

    while priority_queue and (len(visited) < num_nodes):
        current_dist, current_node = heapq.heappop(priority_queue)
        if visited[current_node] == 1:
            continue

        # Update distances for neighboring nodes
        neighbors = edge_index[1][edge_index[0] == current_node]
        wgts  = edge_attr[edge_index[0] == current_node]
        for neighbor, weight in zip(neighbors, wgts):
            if visited[neighbor] == 0:
                new_dist = current_dist + (1.0/np.sqrt(weight))
                if new_dist < distance_map[neighbor]:
                    distance_map[neighbor] = new_dist
                    heapq.heappush(priority_queue, (new_dist, neighbor))

                    if distance_map[current_node]/weight < s[neighbor]:
                        s[neighbor] = distance_map[current_node]/weight
                        label[neighbor] = label[current_node]

        visited[current_node] = 1
    return distance_map, label, len(priority_queue)


class Segmentation:
    def __init__(self, args):
        self.image_path = args.input
        self.ps = args.ps 
        self.label = defaultdict(int)
        self.k = args.k
        self.k_ = args.k_
        self.args = args
        self.best_sig = None
        self.unique_labels = set()
        self.already_loaded = False

    def load_image(self):
        self.img = np.array(Image.open(self.image_path)) / 255.0
        self.img = ((self.img - np.min(self.img)) / (np.max(self.img) - np.min(self.img))).astype("float32")
        self.position = pmat(self.img.shape) 
        self.texture = fmat(self.img)

    def create_seed_mask(self):
        self.seed_img = np.array(Image.open(self.args.mask))
        texture = fmat(self.seed_img)
        self.one = np.all(texture == np.array([0., 0., 0.]), axis=1)
        self.two = np.all(texture == np.array([255., 0., 0.]), axis=1)
        self.three = np.all(texture == np.array([0., 255., 0.]), axis=1)
        self.four = np.all(texture == np.array([0., 0., 255.]), axis=1)
        self.five = np.all(texture == np.array([255., 0., 255.]), axis=1)
        self.six = np.all(texture == np.array([255., 255., 0]), axis=1)
        self.seven = np.all(texture == np.array([0., 255., 255.]), axis=1)
        self.eight = np.all(texture == np.array([255., 0., 125.]), axis=1)
        self.nine = np.all(texture == np.array([255., 125., 0.]), axis=1)
        self.seed_mask = self.one + self.two + self.three + self.four + self.five + self.six + self.seven + self.eight + self.nine

        for ele in np.where(self.one)[0]:
            self.label[ele] = 1
            self.unique_labels.add(1)
        for ele in np.where(self.two)[0]:
            self.label[ele] = 2
            self.unique_labels.add(2)
        for ele in np.where(self.three)[0]:
            self.label[ele] = 3
            self.unique_labels.add(3)
        for ele in np.where(self.four)[0]:
            self.label[ele] = 4
            self.unique_labels.add(4)
        for ele in np.where(self.five)[0]:
            self.label[ele] = 5
            self.unique_labels.add(5)
        for ele in np.where(self.six)[0]:
            self.label[ele] = 6
            self.unique_labels.add(6)
        for ele in np.where(self.seven)[0]:
            self.label[ele] = 7
            self.unique_labels.add(7)
        for ele in np.where(self.eight)[0]:
            self.label[ele] = 8
            self.unique_labels.add(8)
        for ele in np.where(self.nine)[0]:
            self.label[ele] = 9
            self.unique_labels.add(9)

    def nlm(self):
        for i in range(100):
            self.texture = (np.sum(self.texture[self.indices_], axis=1))/(self.k_+1)
        self.texture = (self.texture - np.min(self.texture)) / (np.max(self.texture) - np.min(self.texture))
        self.denoised_texture = self.texture.copy() #lazy

    def create_edge_index_for_nlm(self):
        start = time()
        self.patches = create_patches(self.img, (self.ps, self.ps))
        self.kdt_ = spatial.cKDTree(self.patches)
        distance, self.indices_ = self.kdt_.query(self.patches, self.k_ + 1)
        end = time()
        print("Time taken for filtering:", end-start)

    def estimate_sig(self):
        self.best_sig = 0
        self.max_std = 0
        for sig in [1e-03, 1e-02, 1e-01, 1, 1e+01]:
            test = np.std(np.exp(- self.edge_attr/ sig**2))
            if test > self.max_std:
                self.max_std = test
                self.best_sig = sig
        print(f"The estimated sigma = {self.best_sig:0.2e}. Finetune it using (X * {self.best_sig:0.2e}) where X in range(0.1, 10, 0.1), and inspect visually.")

    def create_edge_index_and_attr(self):
        self.kdt = spatial.cKDTree(self.position)
        distance, indices = self.kdt.query(self.position, self.k + 1)
        s_n = np.repeat(np.arange(len(self.texture)), self.k)
        t_n = indices[:,1:].flatten()
        self.edge_index = np.vstack((s_n, t_n))
        self.distances = np.linalg.norm(self.denoised_texture[indices]-self.denoised_texture[indices][:,0,None], axis=2)[:,1:]
        self.edge_attr = (self.distances.flatten()**2)
        if self.best_sig is None:
            self.estimate_sig()
        if self.args.sig is not None:
            self.edge_attr = np.exp(- self.edge_attr/(self.args.sig)**2)
        else:
            self.edge_attr = np.exp(- self.edge_attr/(self.best_sig)**2)
        self.edge_attr = self.edge_attr + 0.0001 # add noise

    def run_distance_function(self):
        start = time()
        self.distance_map, self.final_label, self.pq_l = distance_map(
            self.edge_index, self.edge_attr, self.seed_mask, self.label
        )
        end = time()
        print("Distance Map Execution Time:", end - start)

    def visualize_segmentation(self):
        seg_img = to_img(np.array([self.final_label[x] for x in range(len(self.patches))]), self.img.shape[:2])
        for i in self.unique_labels:
            mask = (seg_img == i)
            if len(self.img.shape) > 2: # 3 channels
                plt.imsave(f"seg_{i}.png", np.int32(mask)[:,:,np.newaxis]*self.img)
                plt.imshow(np.int32(mask)[:,:,np.newaxis]*self.img)
                plt.axis('off')
            else:
                plt.imsave(f"seg_{i}.png", np.int32(mask)[:,:]*self.img)
                plt.imshow(np.int32(mask)[:,:]*self.img)
                plt.axis('off')
            plt.show()

        plt.imsave(f"seg_image.png", seg_img)
        plt.imshow(seg_img)
        plt.axis('off')
        plt.show()

    def load(self):
        self.load_image()
        self.create_seed_mask()

    def filter(self):
        self.create_edge_index_for_nlm()
        self.nlm()

    def segment(self):
        self.create_edge_index_and_attr()
        self.run_distance_function()
        self.visualize_segmentation()
