package uoft.csc207.fishtank;

import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Typeface;

/**
 * A bubble.
 */
public class Bubble extends TankItem{

    /**
     * How this bubble appears on the screen.
     */
    private String appearance;

    /**
     * Use for random movement left and right.
     */
    private double randMoveVal;

    private Paint paintText = new Paint();

    private FishTankManager fishTank;

    /**
     * Constructs a new bubble at the specified cursor location (x, y).
     */
    Bubble(FishTankManager fishTank) {
        // Get a nice-looking grey for the bubble
        paintText.setTextSize(36);
        paintText.setColor(Color.LTGRAY);
        paintText.setTypeface(Typeface.DEFAULT_BOLD);
        // start off with . as the appearance
        appearance = ".";

        this.fishTank = fishTank;
    }

    /**
     * Set this item's location.
     *
     * @param newX the first coordinate.
     * @param newY the second coordinate.
     */
    void setLocation(int newX, int newY) {
        // set x to newX
        x = newX;
        // set y to newY
        y = newY;
    }

    /**
     * Setter for d.
     *
     * @param randMoveVal new random movement value for the bubble
     */
    void setRandMoveVal(double randMoveVal) {
        this.randMoveVal = randMoveVal;
    }

    /**
     * Draws the given string in the given graphics context at
     * at the given cursor location.
     *
     * @param canvas the graphics context in which to draw the string.
     * @param s      the string to draw.
     * @param x      the x-coordinate of the string's cursor location.
     * @param y      the y-coordinate of the string's cursor location.
     */
    void drawString(Canvas canvas, String s, int x, int y) {
        canvas.drawText(s, x * FishTankView.charWidth, y * FishTankView.charHeight, paintText);
    }


    /**
     * Draws this fish tank item.
     *
     * @param canvas the graphics context in which to draw this item.
     */
    public void draw(Canvas canvas) {
        drawString(canvas, appearance, x, y);
    }

    /**
     * Causes this item to take its turn in the fish-tank simulation.
     */
    void move(){
        if (y <= 0) {
            fishTank.activeFish.remove(this);
            return; //Returns early so following code does'nt run unnecessarily
        }

        if (randMoveVal < 0.33){
            // Move upwards.
            y--;
            // no change left or right

            // Figure out whether to grow, if at all.
            randMoveVal = Math.random();
            // Occasionally change a . to a o or a o to a O
            if (randMoveVal < 0.05) {
                // If the appearance is a ., change it to an o
                if (appearance.equals(".")) appearance = "o";
                    // If the appearance is an o, change it to a O
                else if (appearance.equals("o")) appearance = "O";
            }
        }
        else if(randMoveVal < 0.66){
            // Move upwards.
            y--;
            x += 1;// right
            // Figure out whether to grow, if at all.
            randMoveVal = Math.random();
            // Occasionally change a . to a o or a o to a O
            if (randMoveVal < 0.05) {
                // If the appearance is a ., change it to an o
                if (appearance.equals(".")) appearance = "o";
                    // If the appearance is an o, change it to a O
                else if (appearance.equals("o")) appearance = "O";
            }
        }
        else{
            // Move upwards.
            y--;
            x -= 1; //left

            // Figure out whether to grow, if at all.
            randMoveVal = Math.random();
            // Occasionally change a . to a o or a o to a O
            if (randMoveVal < 0.05) {
                // If the appearance is a ., change it to an o
                if (appearance.equals(".")) appearance = "o";
                    // If the appearance is an o, change it to a O
                else if (appearance.equals("o")) appearance = "O";
            }
        }
    }
}
