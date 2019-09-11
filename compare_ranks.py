import sys

import trectools

if __name__ == '__main__':
    f0 = sys.argv[1]
    f1 = sys.argv[2]
    f2 = sys.argv[3]

    qr = trectools.TrecQrel(f0)
    r1 = trectools.TrecRun(f1)
    r2 = trectools.TrecRun(f2)

    topics = {}
    for i, x in enumerate(r1.run_data.values):
        topic = r1.run_data["query"][i]
        docid = r1.run_data["docid"][i]
        if topic not in topics:
            print(topic)
            topics[topic] = {}
        judgement = qr.get_judgement(docid, topic)
        rank = r1.run_data["rank"][i]
        if judgement > 0:
            topics[topic][docid] = rank

    print(topics)
