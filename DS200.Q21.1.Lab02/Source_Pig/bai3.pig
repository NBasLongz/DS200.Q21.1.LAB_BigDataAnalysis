
-- BÀI 3: KHÍA CẠNH TÍCH CỰC NHẤT & TIÊU CỰC NHẤT

raw = LOAD 'Data/hotel-review.csv' USING PigStorage(';') 
      AS (id:int, review:chararray, category:chararray, aspect:chararray, sentiment:chararray);


-- 3a. SẮP XẾP SỐ ĐÁNH GIÁ NEGATIVE THEO ASPECT

negative_reviews = FILTER raw BY sentiment == 'negative';
neg_grouped = GROUP negative_reviews BY aspect;
neg_count = FOREACH neg_grouped GENERATE group AS aspect, COUNT(negative_reviews) AS neg_total;
neg_sorted = ORDER neg_count BY neg_total DESC;

-- Chỉ cần lưu danh sách tổng đã sắp xếp
STORE neg_sorted INTO 'Output/BaiTap3_NegativeAll' USING PigStorage('\t');


-- 3b. SẮP XẾP SỐ ĐÁNH GIÁ POSITIVE THEO ASPECT

positive_reviews = FILTER raw BY sentiment == 'positive';
pos_grouped = GROUP positive_reviews BY aspect;
pos_count = FOREACH pos_grouped GENERATE group AS aspect, COUNT(positive_reviews) AS pos_total;
pos_sorted = ORDER pos_count BY pos_total DESC;

-- Chỉ cần lưu danh sách tổng đã sắp xếp
STORE pos_sorted INTO 'Output/BaiTap3_PositiveAll' USING PigStorage('\t');
