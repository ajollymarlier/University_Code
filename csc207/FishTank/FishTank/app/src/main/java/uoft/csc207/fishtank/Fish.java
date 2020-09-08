package uoft.csc207.fishtank;

import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Typeface;

/**
 * A fish.
 */
public class Fish extends TankItem{

    /**
     * How this fish appears on the screen.
     */
    String appearance;

    /**
     * Indicates whether this fish is moving right.
     */
    boolean goingRight;

    private Paint paintText = new Paint();

    /**
     * FishTankManager that this Fish is contained in
     */
    FishTankManager fishTank;

    /**
     * Constructs a new fish.
     */
    Fish(FishTankManager fishTank) {
        appearance = "><>";
        paintText.setTextSize(36);
        paintText.setColor(Color.CYAN);
        paintText.setTypeface(Typeface.DEFAULT_BOLD);
        goingRight = true;

        this.fishTank = fishTank;
    }


    /**
     * Set this item's location.
     *
     * @param newX the first coordinate.
     * @param newY the second coordinate.
     */
    void setLocation(int newX, int newY) {
        x = newX;
        y = newY;
    }


    /**
     * Causes this fish to blow a bubble.
     */
    private void blowBubble() {
        Bubble b = new Bubble(fishTank);
        b.setLocation(x, y);
        System.out.println(y + " " + x);

        fishTank.activeFish.add(b);
    }


    /**
     * Build and initialize this fish's forward and backward
     * appearances.
     */
    String reverseAppearance() {
        String reverse = "";
        StringBuilder reverseBuilder = new StringBuilder(reverse);
        for (int i = appearance.length() - 1; i >= 0; i--) {
            switch (appearance.charAt(i)) {
                case ')':
                    reverseBuilder.append('(');
                    break;
                case '(':
                    reverseBuilder.append(')');
                    break;
                case '>':
                    reverseBuilder.append('<');
                    break;
                case '<':
                    reverseBuilder.append('>');
                    break;
                case '}':
                    reverseBuilder.append('{');
                    break;
                case '{':
                    reverseBuilder.append('}');
                    break;
                case '[':
                    reverseBuilder.append(']');
                    break;
                case ']':
                    reverseBuilder.append('[');
                    break;
                default:
                    reverseBuilder.append(appearance.charAt(i));
                    break;
            }
        }

        reverse = reverseBuilder.toString();
        return reverse;
    }

    void turnAround() {
        goingRight = !goingRight;
        appearance = reverseAppearance();
    }

    /**
     * Draws the given string in the given graphics context at
     * at the given cursor location.
     *
     * @param canvas the canvas on which to draw this item.
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
     * @param canvas the canvas on which to draw this item.
     */
    public void draw(Canvas canvas) {
        drawString(canvas, appearance, x, y);
    }


    /**
     * Causes this item to take its turn in the fish-tank simulation.
     */
    public void move() {
        if(x <= 0 || x >= fishTank.getGridWidth())
            turnAround();

        // Figure out whether I turn around.
        double randMoveVal = Math.random();
        if (randMoveVal < 0.1) {
            turnAround();
        }

        // Move one spot to the right or left in the direction I'm going. If I bump into a wall,
        // turn around.
        if (goingRight) {
            x += 1;
        } else {
            x -= 1;
        }

        // Figure out whether I blow a bubble.
        randMoveVal = Math.random();
        if (randMoveVal < 0.1) {
            blowBubble();
        }


        // Figure out whether to move up or down, or neither.
        randMoveVal = Math.random();
        if (randMoveVal < 0.1 && y < fishTank.getGridHeight()) {
            y += 1;
        } else if (randMoveVal < 0.2 && y > 0) {
            y -= 1;
        }
    }
}
