import argparse, glob
import pandas 
import itertools,os
import pdb
import yaml

DEBUG = True

def load_config():
        with open("../../configs/features/opensmile_config.yaml", 'r') as stream:
            parameters = yaml.load(stream)
        
        opensmile = parameters['opensmile']
        features = opensmile['features']
        return features

def process_features(filenames,dir,features):

    print ("Extracting features")
    mean_features = pandas.DataFrame()
    for file in filenames:
        #get the name of the file strip the rest of the path
        print file
        fname = file[file.rfind("/")+1:file.rfind(".")]
        #
        output_dir = os.path.realpath(os.path.join(dir,fname))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        combined = pandas.DataFrame()
        for feature in features:
            f_config = os.path.realpath(os.path.join('..','..','configs','features','opensmile',feature+'.conf'))
            save_as = os.path.realpath(os.path.join(output_dir,feature+'.csv'))
            command = "sudo SMILExtract -C "+ f_config + " -I " + file + " -O " + save_as
            os.system(command)
            df = pandas.read_csv(save_as)
            combined = pandas.concat([combined,df],axis=1)
        final_save_as = os.path.realpath(os.path.join(output_dir,fname+'.csv'))
        combined.to_csv(final_save_as)
        c_mean = combined.mean(axis=0)
        #pdb.set_trace()
        mean_features = pandas.concat([mean_features, c_mean])
        
    mean_save_as = os.path.realpath(os.path.join(dir,'mean_features.csv'))
    mean_features.to_csv(mean_save_as)

def main(input_directory,output_directory,output_extension):
    #load what type of features are to be extracted
    features = load_config()
    print ("OpenSmile features to be extracted : ")
    print (features)

    input_files = glob.glob(os.path.realpath(os.path.join(input_directory,'*.wav')))
    input_files = sorted(input_files)
    print input_files

    #create a directory for saving audio features
    output_dir = os.path.realpath(os.path.join(output_directory,'opensmile_features'))
    #print (output_dir)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    process_features(input_files,output_dir,features)



if __name__ == "__main__":


    parser = argparse.ArgumentParser(description='script for generating traing samples') 
    
    parser.add_argument('-i', '--input_directory', type=str,default=None ,help='The path to the input directory')
    parser.add_argument('-o', '--output_directory', type=str,default=None ,help='The output directory')
    parser.add_argument('-oe', '--output_extension', type=str,default='wav' ,help='The output_extension')

    '''
    python convert_to_wav.py -i data/umich/Clips/Truthful
                             -o data/umich/Audio/Truthful
                             -oe wav  
                             '''


    args = parser.parse_args()

    input_directory = args.input_directory
    output_directory = args.output_directory
    output_extension = args.output_extension

    main(input_directory,output_directory,output_extension)