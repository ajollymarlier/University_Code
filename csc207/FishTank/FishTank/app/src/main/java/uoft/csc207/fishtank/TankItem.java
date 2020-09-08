package uoft.csc207.fishtank;

import android.graphics.Canvas;

public abstract class TankItem {

    /**
     * This item's y-axis coordinate.
     */
    int y;

    /**
     * This item's x-axis coordinate.
     */
    int x;

    /**
     * Draws this fish tank item.  Looks lovely waving in the current, doesn't
     * it?
     *
     * @param canvas the graphics context in which to draw this item.
     */
    public abstract void draw(Canvas canvas);

    /**
     * Draws the given string in the given graphics context at
     * at the given cursor location.
     *
     * @param canvas the graphics context in which to draw the string.
     * @param s      the string to draw.
     * @param x      the x-coordinate of the string's cursor location.
     * @param y      the y-coordinate of the string's cursor location.
     */
    abstract void drawString(Canvas canvas, String s, int y, int x);

    /**
     * Sets new location of TankItem object to parameter values
     *
     * @param newX new value for x-coordinate
     * @param newY      new value for y-coordinate
     */
    abstract void setLocation(int newX, int newY);

    /**
     * Causes this item to take its turn in the fish-tank simulation.
     */
    abstract void move();


}
