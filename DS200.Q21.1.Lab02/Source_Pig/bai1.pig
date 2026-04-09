
raw = LOAD 'Data/hotel-review.csv' 
      USING PigStorage(';') 
      AS (id:int, review:chararray, category:chararray, aspect:chararray, sentiment:chararray);

stopwords = LOAD 'Data/stopwords.txt' AS (word:chararray);

--  Clean text (giữ chữ + space)
clean_review = FOREACH raw GENERATE 
    id,
    REPLACE(LOWER(review), '[^a-zà-ỹ\\s]', '') AS review,
    category, aspect, sentiment;

--  Tokenize
tokens = FOREACH clean_review GENERATE 
    id,
    FLATTEN(TOKENIZE(review)) AS word,
    category, aspect, sentiment;

--  Clean word (fix \r\n + lowercase lại)
tokens_clean = FOREACH tokens GENERATE 
    id,
    LOWER(TRIM(REPLACE(word, '\\r|\\n', ''))) AS word,
    category, aspect, sentiment;

tokens_clean = FILTER tokens_clean BY 
    word IS NOT NULL AND word != '';

--  Stopwords clean
stops = FOREACH stopwords GENERATE 
    LOWER(TRIM(REPLACE(word, '\\r|\\n', ''))) AS stopword;

-- Remove stopwords
joined = JOIN tokens_clean BY word LEFT OUTER, stops BY stopword;
filtered = FILTER joined BY stops::stopword IS NULL;

-- OUTPUT
bai1_out = FOREACH filtered GENERATE 
    tokens_clean::id,
    tokens_clean::word,
    tokens_clean::category,
    tokens_clean::aspect,
    tokens_clean::sentiment;

STORE bai1_out INTO 'Output/BaiTap1' USING PigStorage('\t');
