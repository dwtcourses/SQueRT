#!/usr/bin/env python
# coding: utf-8

# In[1]:

import RelevantSnippets
import albert_QA
import arxiv_pdf_scraper
import ProcessText
import glob
import os
import db_operations


def main(query, keyword):
    pdfdir = os.path.join(os.getcwd(), "Data")
    txtdir = os.path.join(os.getcwd(), "DataTxt")
    csvdir = os.path.join(os.getcwd(), "DataCsv")
    snippetSize = 3

    #Create Table
    db_operations.createTable()

    # Scrape papers to pdf folder
    arxiv_pdf_scraper.scrape(keyword, 1)
    # Convert pdfs to text, then to csv snippets
    for pdfPaperName in glob.glob(pdfdir):
        print(pdfPaperName)
        if not pdfPaperName.endswith(".pdf"):
            print("test1")
        else:
            print("test2")
            ProcessText.pdfToText(pdfPaperName, txtdir)
    for txtPaperName in glob.glob(txtdir + "*.txt"):
        ProcessText.snippetToCsv(txtPaperName, snippetSize, csvdir)
    outputJson = '{ "keyword": ' + '"' + keyword + '" ,' + '"query": ' + '"' + query + '" ,' + '"results": ['
    for csvPaperName in glob.glob(csvdir + "*.csv"):
        relevantSnippets = RelevantSnippets.returnRelevant(csvPaperName, query)
        print(relevantSnippets + "\n\n")
        # From snippets for each paper, return answer
        predictions, snippet = albert_QA.question_answering_albert(query, relevantSnippets)
        paper_identifier = getUrl(csvPaperName)
        outputJson += '{' + \
                      '"predictions": ' + '"' + predictions + '" ,' + \
                      '"snippet": ' + '"' + snippet + '" ,' + \
                      '"paper_identifier": ' + '"' + paper_identifier + '" },'
        print(predictions)
        print(snippet)
    outputJson += '] }'
    # removing the last comma
    lastCommaIndex = outputJson.rfind(",")
    resultJson = outputJson[:lastCommaIndex] + "" + outputJson[lastCommaIndex + 1:]
    print(resultJson)
    # paper_identifier and snippet need to be returned from above methods
    return resultJson


def save_feedback(topic, query, feedback):
    db_operations.updateRecords(topic, query, feedback)
    print('Feedback saved!')

def getUrl(csvPaperName):
    url = 'http://localhost:8080/Data/'
    fileName = csvPaperName.rsplit('_', 1)[0] +'.pdf'
    url +=fileName
    return url

main("What model is best for large batch training for bert", "Machine learning")

#pdfdir = os.path.join(os.getcwd(), "Data")
#print(pdfdir)
#for pdfPaperName in glob.glob(pdfdir):
#    print("Hello there!")

#if __name__ == "__main__":
#    main(query, topic)