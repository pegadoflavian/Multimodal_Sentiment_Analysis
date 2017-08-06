import os
import argparse, glob

def convert_to_wav(input_file,output_file):
    command = "ffmpeg -i "+input_file+ " "+output_file
    os.system(command)

def main(input_directory,output_directory,input_extension,output_extension):

    input_files = glob.glob(input_directory+"/*."+input_extension)
    input_files = sorted(input_files)
    

    count = 0

    for input_file in input_files:

        print "converting file " + str(count+1) +" of " + str(len(input_files))

        temp = input_file[input_file.rfind("/")+1 :input_file.rfind(".")]
        output_file = output_directory + "/"+ temp+"."+output_extension
        convert_to_wav(input_file,output_file)

        count +=1

if __name__ == "__main__":


    parser = argparse.ArgumentParser(description='script for generating traing samples') 
    
    parser.add_argument('-i', '--input_directory', type=str,default=None ,help='The path to the input directory')
    parser.add_argument('-o', '--output_directory', type=str,default=None ,help='The output directory')
    parser.add_argument('-ie', '--input_extension', type=str,default=None ,help='The input extension')
    parser.add_argument('-oe', '--output_extension', type=str,default='wav' ,help='The output_extension')

    '''
    python convert_to_wav.py -i data/umich/Clips/Truthful
                             -o data/umich/Audio/Truthful
                             -ie mp4
                             -oe wav  
                             '''


    args = parser.parse_args()

    input_directory = args.input_directory
    output_directory = args.output_directory
    input_extension = args.input_extension
    output_extension = args.output_extension

    main(input_directory,output_directory,input_extension,output_extension)
    