import sys, getopt, project

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hf:n:m:M:",["function="])
    except getopt.GetoptError:
        print('project.py -f <function>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print('project.py -f <function> -n <num_responses> -m <model_name> -M <model_name_array>')
            print('\t-f <function> - str - required - function name\n\t\toptions: ["create_training_file", "emulate_vibe", "compare_vibes"]')
            print('\t-n <num_responses> - int - default 1 - number of responses desired')
            print('\t-m <model_name> - str - default "theonion" - key value name for model')
            print('\t-M <model_array> - arr - default new_models - array of string model names')
            sys.exit()
        elif opt in ("-f", "--function"):
            function = arg
            num_responses = 1
            model_name = 'theonion'
            model_array = None
        elif opt in ("-n", "--num_responses"):
            num_responses = int(arg)
        elif opt in ("-m", "--model_name"):
            model_name = str(arg)
        elif opt in ("-M", "--model_array"):
            model_array = arg
    match function:
        case "create_training_file":
            project.create_training_file()
        case "emulate_vibe":
            project.emulate_vibe(num_responses, model_name)
        case "compare_vibes":
            project.compare_vibes(model_array)
        case _:
            print("Invalid input for -f function flag\n")
            sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])