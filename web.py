import json, argparse, os
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html', relation_length = len(relations))

@app.route("/<int:sentence_id>", methods=['POST', 'GET'])
def start(sentence_id):
    done = False

    if request.method == 'POST':
        form = request.form

        # we are starting at a different sentence
        if 'sentence_id' in form:
            sentence_id = int(form['sentence_id']) - 1

        else:
            index = int(form['index'])
            # tagging is canceled
            if form['submit'] == 'cancel':
                write_relations()
                done = True

            # all sentences are tagged
            elif index + 1 >= len(relations):
                update_relations(form)
                write_relations()

            # display the next sentence
            elif form['submit'] == 'next':
                update_relations(form)
                write_relations()

    current_result = None
    if sentence_id < len(results):
        current_result = results[sentence_id]['relations']

    return render_template('sentence.html', done = done, relations = relations, current_result = current_result, index = sentence_id, relation_length = len(relations), results_length = len(results))


def write_relations():
    with open(json_results_file, 'w') as outfile:
        json.dump(results, outfile)


def update_relations(form):
    index = int(form['index'])

    result = []
    for rel in relations[index]['relations']:
        correct = "none"
        informative = "none"
        coherent = "none"
        factual = "none"
        not_sure = "none"
        other = "none"

        rel_id = rel['id']

        # relation informative, coherent, factual, ok?
        form_key = 'relation-' + str(rel_id) + '-info'
        if form_key in form:
            l = form.getlist(form_key)
            if "uninformative" in l:
                informative = 'False'
                correct = 'False'
            if "incoherent" in l:
                coherent = 'False'
                correct = 'False'
            if "nonfactual" in l:
                factual = 'False'
                correct = 'False'
            if "correct" in l:
                correct = 'True'
            if "not-sure" in l:
                not_sure = 'True'
            if "other" in l:
                other = 'True'

        result.append({
            "id": rel_id,
            "correct": correct,
            "informative": informative,
            "coherent": coherent,
            "factual": factual,
            "not-sure": not_sure,
            "other": other
        })

    # add the results
    result_object = find_result_object(index)
    if result_object is not None:
        result_object['relations'] = result
    else:
        result_object = {
            "sentenceId" : relations[index]['sentenceId'],
            "companyId"  : relations[index]['companyId'],
            "webpageId"  : relations[index]['webpageId'],
            "relations"  : result
        }
        results.append(result_object)


def find_result_object(index):
    for r in results:
        if r['companyId'] != relations[index]['companyId']:
            continue
        if r['webpageId'] != relations[index]['webpageId']:
            continue
        if r['sentenceId'] != relations[index]['sentenceId']:
            continue
        return r
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='run the web demo', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-p", "--person", action="store", required=True, dest="person", help="Are you 'stefan', 'dominik', 'rice', 'joseph', 'tim', 'michael', 'toni', 'anja', 'max', 'thorsten', 'sebastian' or 'tanja'?")
    args = parser.parse_args()

    if args.person not in ['stefan', 'michael', 'joseph', 'rice', 'dominik', 'tanja', 'tim', 'toni', 'thorsten', 'anja', 'max', 'sebastian']:
        args.print_help()
        sys.exit()
    else:
        json_relation_file = "data/" + args.person + "/relations.json"
        json_results_file = "data/" + args.person + "/output.json"

    #### read relations ####
    relations = []
    with open(json_relation_file) as data_file:
        relations = json.load(data_file)
    #### read results ####
    results = []
    with open(json_results_file) as data_file:
        results = json.load(data_file)

    #### start app ####
    app.run(host = "0.0.0.0")
