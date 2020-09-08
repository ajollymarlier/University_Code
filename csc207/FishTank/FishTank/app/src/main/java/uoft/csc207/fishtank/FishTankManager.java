package uoft.csc207.fishtank;

import android.graphics.Canvas;

import java.util.ArrayList;

class FishTankManager {

    /**
     * All the locations where a fish can be.
     */
    ArrayList<TankItem> activeFish;
    /**
     * The width of activeFish.
     */
    private int gridWidth;
    /**
     * The height of activeFish.
     */
    private int gridHeight;


    /**
     * Return the width of a row of locations.
     *
     * @return the width of a column of locations.
     */
    int getGridWidth() {
        return gridWidth;
    }

    /**
     * Return the height of a column of locations.
     *
     * @return the height of a column of locations.
     */
    int getGridHeight() {
        return gridHeight;
    }

    /**
     * The fish tank manager on a screen with height rows and width columns.
     */
    FishTankManager(int height, int width) {
        gridHeight = height;
        gridWidth = width;
        activeFish = new ArrayList<>();
    }

    void draw(Canvas canvas) {
        for (int i = 0; i < activeFish.size(); i++) {
                if (activeFish.get(i) != null){
                    if (activeFish.get(i) instanceof Bubble) {
                        Bubble bubble = (Bubble) activeFish.get(i);
                        bubble.draw(canvas);
                    }
                    else
                        activeFish.get(i).draw(canvas);
                }
        }
    }

    void update() {
        for (int i = 0; i < activeFish.size(); i++) {
                if (activeFish.get(i) != null)
                    if (activeFish.get(i) instanceof Bubble) {
                        // Figure out whether to float left or right, if at all.
                        Bubble bubble = (Bubble) activeFish.get(i);
                        bubble.setRandMoveVal(Math.random());
                        bubble.move();
                    } else {
                        activeFish.get(i).move();
                    }
        }
    }

    void createTankItems() {
        activeFish.add(new Fish(this));
        activeFish.get(activeFish.size() - 1).setLocation(28, 18);

        activeFish.add(new Fish(this));
        activeFish.get(activeFish.size() - 1).setLocation(10, 22);

        activeFish.add(new Fish(this));
        activeFish.get(activeFish.size() - 1).setLocation(17, 14);

        activeFish.add(new Fish(this));
        activeFish.get(activeFish.size() - 1).setLocation(15, 28);

        activeFish.add(new Fish(this));
        activeFish.get(activeFish.size() - 1).setLocation(35, 36);

        activeFish.add(new Fish(this));
        activeFish.get(activeFish.size() - 1).setLocation(16, 5);

        activeFish.add(new Fish(this));
        activeFish.get(activeFish.size() - 1).setLocation(16, 12);

        activeFish.add(new Fish(this));
        activeFish.get(activeFish.size() - 1).setLocation(16, 18);

        activeFish.add(new Fish(this));
        activeFish.get(activeFish.size() - 1).setLocation(23, 18);

        activeFish.add(new Fish(this));
        activeFish.get(activeFish.size() - 1).setLocation(6, 12);

        activeFish.add(new HungryFish(this));
        activeFish.get(activeFish.size() - 1).setLocation(10, 20);

        activeFish.add(new VeggieFish(this));
        activeFish.get(activeFish.size() - 1).setLocation(20, 40);

        activeFish.add(new Seaweed(9));
        activeFish.get(activeFish.size() - 1).setLocation(33, 4);

        activeFish.add(new Seaweed(6));
        activeFish.get(activeFish.size() - 1).setLocation(24, 13);

        activeFish.add(new Seaweed(12));
        activeFish.get(activeFish.size() - 1).setLocation(42, 15);

        activeFish.add(new Seaweed(5));
        activeFish.get(activeFish.size() - 1).setLocation(13, 20);
    }
}
