package model;

import java.io.Serializable;

public class RatingStats implements Serializable {
    public double sum;
    public int count;

    public RatingStats(double sum, int count) {
        this.sum = sum;
        this.count = count;
    }

    public static RatingStats merge(RatingStats a, RatingStats b) {
        return new RatingStats(a.sum + b.sum, a.count + b.count);
    }

    public double getAverage() {
        return count == 0 ? 0 : sum / count;
    }
}