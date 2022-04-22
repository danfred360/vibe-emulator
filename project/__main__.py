import sys, getopt, project

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hf:n:m:M:",["function="])
    except getopt.GetoptError:
        print('Bad args: "vibe-emulator -h" for help')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print('vibe-emulator -f <function> -n <num_responses> -m <model_name> -M <model_name_array>')
            print('\t-f <function> - str - required - function name\n\t\toptions: ["create_training_file", "emulate_vibe", "compare_vibes"]')
            print('\t-n <num_responses> - int - default 1 - number of responses desired')
            print('\t-m <model_name> - str - default "theonion" - key value name for model')
            print('\t-M <model_array> - arr - default new_models - array of string model names')
            sys.exit()
        elif opt in ("-f", "--function"):
            function = arg
            num_responses = 1
            model_name = 'theonion'
            model_list_name = 'default'
        elif opt in ("-n", "--num_responses"):
            num_responses = int(arg)
        elif opt in ("-m", "--model_name"):
            model_name = str(arg)
        elif opt in ("-l", "--model_list"):
            model_list_name = arg
    match function:
        case "create_model":
            project.create_model()
        case "emulate_vibe":
            project.emulate_vibe(num_responses, model_list_name, model_name)
        case "compare_vibes":
            project.compare_vibes(num_responses, model_list_name)
        case _:
            print("Invalid input for -f function flag\n")
            sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])