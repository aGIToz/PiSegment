import argparse
from pisegment.annotator import create_mask
from pisegment.segmentation import Segmentation 

def main():
    parser = argparse.ArgumentParser(description='Create a mask on an image.')
    parser.add_argument('--input', type=str, help='Path to the image to be annotated.')
    parser.add_argument('--mask', type=str, help='Path where the generated mask image will be saved.')
    parser.add_argument('--ps', type=int, default=3, help='The pacth size for denoising.')
    parser.add_argument('--k', type=int, default=4,help='The k in knn for segmentation using distance function.')
    parser.add_argument('--k_', type=int, default=10,help='The k in knn for denoising.')
    parser.add_argument('--sig', type=float, help='Sigma value in RBF kernel for segmentation.')
    parser.add_argument('--no_filter', action='store_true', help='No filter before segmentation')

    args = parser.parse_args()
    create_mask(args.input, args.mask)
    seg_obj = Segmentation(args)
    seg_obj.load()
    if args.no_filter: 
        pass
    else:
        seg_obj.filter()
    seg_obj.segment()

if __name__ == "__main__":
    main()
