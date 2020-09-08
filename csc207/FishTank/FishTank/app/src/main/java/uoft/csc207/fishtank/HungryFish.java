package uoft.csc207.fishtank;

class HungryFish extends Fish {

    /**
     * Constructs a new hungry fish.
     */

    HungryFish(FishTankManager fishTank) {
        super(fishTank);

        appearance = "><MEHUNGRY>";
    }

    /**
     * Build and initialize this fish's forward and backward
     * appearances.
     */
    String reverseAppearance() {
        System.out.println("Turning around" + this.appearance);
        String reverse = super.reverseAppearance();

        System.out.println("Turned around" + this.appearance);
        appearance = reverse;
        return reverse;
    }
}
