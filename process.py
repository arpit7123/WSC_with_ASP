import re
import json
import subprocess
from os import listdir
from os.path import isfile,join

def main(input_file):
    f = open(input_file,'r')
    probs_arr = json.load(f)
    counter = 1
    for prob in probs_arr:
        print("SOLVING: " + str(counter))
        pronoun = prob["pronoun"]
        ans_ch1 = prob["ans_ch1"]
        ans_ch2 = prob["ans_ch2"]
        #if "parser_output" in prob:
        if "wsc_sent_rep" in prob:
            s_rep = prob["wsc_sent_rep"]
        else:
            print("DOES NOT CONTAIN WSC PARSE!")
            counter+=1
            continue

        #if "k_parser_out" in prob:
        if "know_sent_rep" in prob:
            k_rep = prob["know_sent_rep"]
        else:
            print("DOES NOT CONTAIN KNOWLEDGE PARSE!")
            counter+=1
            continue
        
        coref1 = prob["coref1"]
        coref2 = prob["coref2"]
    
        asp_input_arr = []
        asp_input_arr.append("pronoun(\"" + pronoun + "\").")
        asp_input_arr.append("ans_ch1(\"" + ans_ch1 + "\").")
        asp_input_arr.append("ans_ch2(\"" + ans_ch2 + "\").")

        for s_r in s_rep:
            s_r = s_r.replace(",","\",\"")
            s_r = s_r.replace("(","(\"")
            s_r = s_r.replace(")","\")")
            asp_input_arr.append("has_s" + s_r)

        for k_r in k_rep:
            k_r = k_r.replace(",","\",\"")
            k_r = k_r.replace("(","(\"")
            k_r = k_r.replace(")","\")")
            asp_input_arr.append("has_k" + k_r)
        
        asp_input_arr.append("has_k(\"" + coref1 +"\",\"is_same_as\",\"" + coref2 + "\").")
        asp_input_arr.append("has_k(\"" + coref2 +"\",\"is_same_as\",\"" + coref1 + "\").")
        
        #for a  in asp_input_arr:
        #    print(a)
        
        temp_file = "temp.txt"
        f_w = open(temp_file,'w')
        for a in asp_input_arr:
            f_w.write(a+"\n")
        f_w.close()

        execute_clingo(temp_file)
        counter+=1

def execute_clingo(in_file):
    curr_dir = "/home/arpit/workspace/WinogradPhd/WebContent/WEB-INF/lib/WSC_data/wsc_may02_2019/kparser_jsons/with_knowledge"
    clingo_exec_file = "/home/arpit/workspace/WinogradPhd/WebContent/WEB-INF/lib/Clingo/clingo"
    asp_rules_file = "/home/arpit/workspace/WinogradPhd/WebContent/WEB-INF/lib/WSC_data/wsc_may02_2019/kparser_jsons/with_knowledge/asp_rules"
    asp_input_file = in_file
    
    bashCommand = clingo_exec_file + " " + asp_rules_file + " " + asp_input_file + " 0"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE, cwd = curr_dir)
    output, error = process.communicate()
    
    anss = re.findall(r'ans\((.*?)\)',output)
    s = set()
    for ans in anss:
        s.add(ans)
        #print(ans)

    if len(s)==1:
        print("Answer is: " + anss[0])
    else:
        print("No Answer")

    #print(output)

if __name__=="__main__":
    #main("test.json")
    #main("./done/type9_sents_step2_triples_know.json")
    main("./done/combined_probs.json")
    #main("./done/test.json")
    #execute_clingo("./test")

    #aa = re.findall( r'all (.*?) are', 'all cats are smarter than dogs, all dogs are dumber than cats')
    #for a in aa:
    #    print(a)




