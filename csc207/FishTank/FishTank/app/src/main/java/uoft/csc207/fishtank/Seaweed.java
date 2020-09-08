package uoft.csc207.fishtank;

import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Typeface;

public class Seaweed extends TankItem{
    private Paint paintText = new Paint();

    /**
     * The number of weed segments.
     */
    private int numSegments;

    /**
     * Indicates whether the bottom segment is leaning right.
     */
    private boolean leanRight;

    /**
     * Constructs a new seaweed item at the specified cursor
     * location (x,y),l segments tall.
     * @param numSegments the number of segments this seaweed is tall.
     */
    Seaweed(int numSegments) {
        this.numSegments = numSegments;
        paintText.setTextSize(36);
        paintText.setColor(Color.GREEN);
        paintText.setTypeface(Typeface.DEFAULT_BOLD);
    }

    /**
     * Draws this fish tank item.  Looks lovely waving in the current, doesn't
     * it?
     *
     * @param canvas the graphics context in which to draw this item.
     */
    public void draw(Canvas canvas) {

        // WWhich way does the first segment lean?
        boolean lR = leanRight;

        for (int i = 0; i < numSegments; i++) {// Draw a "/" seaweed segment: even numbered and leaning to the right.
            if (i % 2 == 0){
                if (lR)
                    drawString(canvas, "/", x, -i + y);
                else
                    // Draw the string
                    drawString(canvas, "\\", x, -i + y);
            }

            else{
                if (lR)
                    // Draw the string
                    drawString(canvas, "\\", x, -i + y);
            }
        }
    }

    /**
     * Draws the given string in the given graphics context at
     * at the given cursor location.
     *
     * @param canvas where to draw the string.
     * @param s      the string to draw.
     * @param x      the x-coordinate of the string's cursor location.
     * @param y      the y-coordinate of the string's cursor location.
     */
    void drawString(Canvas canvas, String s, int x, int y) {
        canvas.drawText(s, x * FishTankView.charWidth, y * FishTankView.charHeight, paintText);
    }


    /**
     * Set this item's location.
     *
     * @param newX the first coordinate.
     * @param newY the second coordinate.
     */
    void setLocation(int newX, int newY) {
        this.x = newX;
        this.y = newY;
    }

    /**
     * Causes this item to take its turn in the fish-tank simulation.
     */
    void move() {
        leanRight = !leanRight;
    }

}