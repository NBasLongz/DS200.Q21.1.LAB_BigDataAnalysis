
-- BÀI 4: TOP 5 TỪ TÍCH CỰC / TIÊU CỰC THEO CATEGORY

%declare INPUT_PATH 'Output/BaiTap1'
%declare POS_OUTPUT 'Output/BaiTap4_top5_positive'
%declare NEG_OUTPUT 'Output/BaiTap4_top5_negative'

data = LOAD '$INPUT_PATH' USING PigStorage('\t') 
       AS (id:int, word:chararray, category:chararray, aspect:chararray, sentiment:chararray);

-- 4A. POSITIVE
pos_words  = FILTER data BY sentiment == 'positive';
pos_counts = FOREACH (GROUP pos_words BY (category, word)) 
             GENERATE FLATTEN(group) AS (category, word), COUNT(pos_words) AS freq;
pos_top5   = FOREACH (GROUP pos_counts BY category) {
    sorted = ORDER pos_counts BY freq DESC;
    top5   = LIMIT sorted 5;
    GENERATE FLATTEN(top5);
};
STORE pos_top5 INTO '$POS_OUTPUT' USING PigStorage('\t');

-- 4B. NEGATIVE
neg_words  = FILTER data BY sentiment == 'negative';
neg_counts = FOREACH (GROUP neg_words BY (category, word)) 
             GENERATE FLATTEN(group) AS (category, word), COUNT(neg_words) AS freq;
neg_top5   = FOREACH (GROUP neg_counts BY category) {
    sorted = ORDER neg_counts BY freq DESC;
    top5   = LIMIT sorted 5;
    GENERATE FLATTEN(top5);
};
STORE neg_top5 INTO '$NEG_OUTPUT' USING PigStorage('\t');

