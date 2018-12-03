#! /bin/bash

langue=fr
tool=/home/cindy/Documents/macaon_data/$langue/bin/maca_tm_tagparser

$tool bad.txt columns.mcd --sequenceDelimiterTape FORM --sequenceDelimiter ? --printEntropy 2> parsed_questions.txt
tail +4 parsed_questions.txt > bad_entropies
rm parsed_questions.txt


$tool good.txt columns.mcd --sequenceDelimiterTape FORM --sequenceDelimiter ? --printEntropy 2> parsed_questions.txt
tail +4 parsed_questions.txt > good_entropies
rm parsed_questions.txt

#maca_tm_tagparser bad.txt columns.mcd --sequenceDelimiterTape FORM --sequenceDelimiter ? > tmp
#mv tmp bad.txt
#maca_tm_tagparser good.txt columns.mcd --sequenceDelimiterTape FORM --sequenceDelimiter ? > tmp
#mv tmp good.txt
