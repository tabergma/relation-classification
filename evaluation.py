import json


if __name__ == "__main__":

    groups = [('michael', 'stefan'), ('dominik', 'rice'), ('joseph','tim'), ('anja', 'max'), ('thorsten', 'sebastian')]

    overall_total = 0
    overall_agreement = 0
    overall_ok = 0

    for group in groups:
        json_out_file_1 = "data/" + group[0] + "/output.json"
        json_out_file_2 = "data/" + group[1] + "/output.json"

        results_1 = []
        with open(json_out_file_1) as data_file:
            results_1 = json.load(data_file)
        results_2 = []
        with open(json_out_file_2) as data_file:
            results_2 = json.load(data_file)

        total = 0
        agreement = 0
        error_agreement = 0
        uninformative = 0
        nonfactual = 0
        incoherent = 0
        other = 0
        ok = 0
        not_sure = 0

        for a, b in zip(results_1, results_2):

            if a['webpageId'] != b['webpageId'] or a['sentenceId'] != b['sentenceId'] or a['companyId'] != b['companyId']:
                print("Not the same sentence!")
                print(a, b)
                continue

            for a_rel, b_rel in zip(a['relations'], b['relations']):

                if a_rel['id'] != b_rel['id']:
                    print("Not the same relation!")
                    print(a, b)
                    continue

                total += 1

                if a_rel['correct'] == b_rel['correct'] == 'True':
                    agreement += 1
                    ok += 1

                elif a_rel['correct'] == b_rel['correct'] == 'False':
                    agreement += 1

                    same_error = False
                    if a_rel['informative'] == b_rel['informative'] == 'False':
                        uninformative += 1
                        same_error = True
                    if a_rel['coherent'] == b_rel['coherent'] == 'False':
                        incoherent += 1
                        same_error = True
                    if a_rel['factual'] == b_rel['factual'] == 'False':
                        nonfactual += 1
                        same_error = True
                    if a_rel['other'] == b_rel['other'] == 'False':
                        other += 1
                        same_error = True

                    if same_error:
                        error_agreement += 1

                elif a_rel['correct'] == b_rel['correct'] == 'none' and a_rel['not-sure'] == b_rel['not-sure'] == 'True':
                    not_sure += 1
                    agreement += 1

        print("")
        print("Group" + str(group))
        print("Agreement: " + str(agreement) + "/" + str(total))
        print("Error Agreement:" + str(error_agreement) + "/" + str(agreement - ok))
        print("Ok: " + str(ok))
        print("Uninformative: " + str(uninformative))
        print("Incoherent: " + str(incoherent))
        print("Non-Factual: " + str(nonfactual))
        print("Other Errors: " + str(other))
        print("Not Sure: " + str(not_sure))

        overall_agreement += agreement
        overall_ok += ok
        overall_total += total


    print("")
    print("")
    print("RESULT")
    print("Agreement: " + str(overall_agreement) + "/" + str(overall_total))
    print("Ok: " + str(overall_ok))
