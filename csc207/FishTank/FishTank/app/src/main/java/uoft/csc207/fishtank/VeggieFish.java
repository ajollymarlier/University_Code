package uoft.csc207.fishtank;

public class VeggieFish extends Fish {
    /**
     * Seaweed object that ths Fish is moving towards
     */
    private Seaweed targetFood;

    /**
     * Boolean value for if a Seaweed object exists in activeFish list
     */
    private boolean targetExists;

    /**
     * Constructs a new fish.
     *
     * @param fishTank // FishTankManager that this Fish is contained in
     */
    VeggieFish(FishTankManager fishTank) {
        super(fishTank);

        targetExists = true;
        appearance = "><VEGGIE>";
    }

    /**
     * Build and initialize this fish's forward and backward
     * appearances.
     */
    String reverseAppearance() {
        System.out.println("Turning veggie around" + this.appearance);
        String reverse = super.reverseAppearance();

        System.out.println("Turned veggie around" + this.appearance);
        appearance = reverse;
        return reverse;
    }

    /**
     * Moves fish towards target Seaweed targetFood
     */
    @Override
    public void move() {
        if(targetFood != null){ //If VeggieFish has a target
            if(targetFood.x - x != 0) // Deals with divide by 0 case
                x += (targetFood.x - x) / Math.abs(targetFood.x - x); //Returns signed value of 1

            if(targetFood.y - y != 0)
                y += (targetFood.y - y) / Math.abs(targetFood.y - y);

            //Checks if VeggieFish eats Seaweed
            if (x == targetFood.x && y == targetFood.y) {
                fishTank.activeFish.remove(targetFood);
                targetFood = null;
                targetExists = false;
            }

        }else{
            for (int i = 0; i < fishTank.activeFish.size(); i++){
                if (fishTank.activeFish.get(i) instanceof Seaweed) {
                    targetFood = (Seaweed) fishTank.activeFish.get(i);
                    targetExists = true;
                }
            }

            //If no more seaweed exists, this Fish acts like a normal fish
            if (!targetExists) {
                super.move();
                return;
            }

            //If target exists after searching
            if(targetFood != null){
                if (targetFood.x - x < 0 && goingRight)
                    turnAround();

                else if (targetFood.x - x > 0 && !goingRight)
                    turnAround();
            }else{
                targetExists = false;
            }
        }
    }
}
