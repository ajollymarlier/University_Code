import java.sql.*;
import java.util.Date;
import java.util.Arrays;
import java.util.List;

public class Assignment2 {

   // A connection to the database
   Connection connection;

   // Can use if you wish: seat letters
   List<String> seatLetters = Arrays.asList("A", "B", "C", "D", "E", "F");

   Assignment2() throws SQLException {
      try {
         Class.forName("org.postgresql.Driver");
      } catch (ClassNotFoundException e) {
         e.printStackTrace();
      }
   }

   /**
    * Connects and sets the search path.
    *
    * Establishes a connection to be used for this session, assigning it to the
    * instance variable 'connection'. In addition, sets the search path to
    * 'air_travel, public'.
    *
    * @param url      the url for the database
    * @param username the username to connect to the database
    * @param password the password to connect to the database
    * @return true if connecting is successful, false otherwise
    */
   public boolean connectDB(String URL, String username, String password) {
      try {
         connection = DriverManager.getConnection(URL, username, password);
      } catch (SQLException ex) {
         return false;
      }

      return true;
   }

   /**
    * Closes the database connection.
    *
    * @return true if the closing was successful, false otherwise
    */
   public boolean disconnectDB() {
      // Implement this method!
      try {
         connection.close();
      } catch (SQLException ex) {
         return false;
      }

      return true;
   }

   /* ======================= Airline-related methods ======================= */

   /**
    * Attempts to book a flight for a passenger in a particular seat class. Does so
    * by inserting a row into the Booking table.
    *
    * Read handout for information on how seats are booked. Returns false if seat
    * can't be booked, or if passenger or flight cannot be found.
    *
    * 
    * @param passID    id of the passenger
    * @param flightID  id of the flight
    * @param seatClass the class of the seat (economy, business, or first)
    * @return true if the booking was successful, false otherwise.
    */
   public boolean bookSeat(int passID, int flightID, String seatClass) {
      // Implement this method!
      String overbooksSqlStr = "select p.capacity_business, p.capacity_first, p.capacity_economy, b.datetime booking_time, b.id booking_id, economy_attendance, business_attendance, first_attendance, f.id flight_id "
            + "from booking b " + "inner join flight f on f.id = b.flight_id "
            + "inner join plane p on p.tail_number = f.plane "
            + "inner join (select count(seat_class) business_attendance, flight_id " + "from booking "
            + "where seat_class = 'business' "
            + "group by flight_id, seat_class) business_attendance on business_attendance.flight_id = f.id "
            + "inner join (select count(seat_class) first_attendance, flight_id " + "from booking "
            + "where seat_class = 'first' "
            + "inner join (select count(seat_class) economy_attendance, flight_id " + "from booking "
            + "where seat_class = 'economy' "
            + "group by flight_id, seat_class) first_attendance on first_attendance.flight_id = f.id "
            + "where f.id = " + flightID + " order by b.datetime;";

      try {
         PreparedStatement execStatCapacity = connection.prepareStatement(overbooksSqlStr);
         ResultSet capacities = execStatCapacity.executeQuery();
         capacities.next();

         if(seatClass.equals("economy") && capacities.getInt("capacity_economy") + 10 > capacities.getInt("economy_attendance")){
            //book economy flight with over booking rules
            bookSeatHelper(passID, flightID, seatClass);
         }
         else if(seatClass.equals("business") && capacities.getInt("capacity_business")> capacities.getInt("business_attendance")){
            //Book business flight
            bookSeatHelper(passID, flightID, seatClass);

         }
         else if(seatClass.equals("first") && capacities.getInt("capacity_first")> capacities.getInt("first_attendance")){
            //Book first flight
            bookSeatHelper(passID, flightID, seatClass);

         }
         else{
            return false;
         }

      } catch (SQLException e) {
         return false;
      }

      return true;
   }

   /**
    * Attempts to upgrade overbooked economy passengers to business class or first
    * class (in that order until each seat class is filled). Does so by altering
    * the database records for the bookings such that the seat and seat_class are
    * updated if an upgrade can be processed.
    *
    * Upgrades should happen in order of earliest booking timestamp first.
    *
    * If economy passengers left over without a seat (i.e. more than 10 overbooked
    * passengers or not enough higher class seats), remove their bookings from the
    * database.
    * 
    * @param flightID The flight to upgrade passengers in.
    * @return the number of passengers upgraded, or -1 if an error occured.
    */
   public int upgrade(int flightID) {
      // Implement this method!
      String overbooksSqlStr = "select p.capacity_business, p.capacity_first, b.datetime booking_time, b.id booking_id, business_attendance, first_attendance, f.id flight_id "
            + "from booking b " + "inner join flight f on f.id = b.flight_id "
            + "inner join plane p on p.tail_number = f.plane "
            + "inner join (select count(seat_class) business_attendance, flight_id " + "from booking "
            + "where seat_class = 'business' "
            + "group by flight_id, seat_class) business_attendance on business_attendance.flight_id = f.id "
            + "inner join (select count(seat_class) first_attendance, flight_id " + "from booking "
            + "where seat_class = 'first' "
            + "group by flight_id, seat_class) first_attendance on first_attendance.flight_id = f.id "
            + "where (row is NULL) and (letter is NULL) and f.id = " + flightID + " order by b.datetime;";

      int numUpgraded = 0;
      try {
         PreparedStatement execStatOverbook = connection.prepareStatement(overbooksSqlStr);
         ResultSet overbooks = execStatOverbook.executeQuery();

         int capacity_business;
         int capacity_first;
         int booking_id;
         int business_attendance;
         int first_attendance;
         
         while (overbooks.next()) {
            // Get values and check capcities to then update
            capacity_business = overbooks.getInt("capacity_business");
            capacity_first = overbooks.getInt("capacity_business");
            booking_id = overbooks.getInt("booking_id");
            business_attendance = overbooks.getInt("business_attendance");
            first_attendance = overbooks.getInt("flight_id");

            if (capacity_business > business_attendance) {
               upgradeHelper("business", booking_id);
               numUpgraded++;
            }else if(capacity_first > first_attendance){
               upgradeHelper("first", booking_id);
               numUpgraded++;
            }
         }
      } catch (SQLException ex) {
         return -1;
      }

      return numUpgraded;
   }

   /* ----------------------- Helper functions below ------------------------- */

   // A helpful function for adding a timestamp to new bookings.
   // Example of setting a timestamp in a PreparedStatement:
   // ps.setTimestamp(1, getCurrentTimeStamp());

   /**
    * Returns a SQL Timestamp object of the current time.
    * 
    * @return Timestamp of current time.
    */
   private java.sql.Timestamp getCurrentTimeStamp() {
      java.util.Date now = new java.util.Date();
      return new java.sql.Timestamp(now.getTime());
   }

   private void bookSeatHelper(int pass_id, int flight_id, String seat_class){
      try {
         String seatQuery = "select max(row) max_row, max(letter) max_letter, max(id) from booking where seat_class = '" +
                          seat_class + "';";
         PreparedStatement execStatMaxSeat = connection.prepareStatement(seatQuery);
         ResultSet maxSeat = execStatMaxSeat.executeQuery();
         maxSeat.next();
         
         int maxSeatRow = maxSeat.getInt("max_row");
         String maxSeatLetter = maxSeat.getString("max_letter");
         int maxId = maxSeat.getInt("id");

         int newSeatRow;
         String newSeatLetter;
         if(maxSeatLetter.equals("F")){
            newSeatRow = maxSeatRow + 1;
            newSeatLetter = "A";
         }else{
            newSeatRow = maxSeatRow;
            newSeatLetter = seatLetters.get(seatLetters.indexOf(maxSeatLetter) + 1);
         }

         String getPriceSQLStatement = "select " + seat_class + " from price where flight_id = " + flight_id;
         PreparedStatement execStatGetPrice = connection.prepareStatement(getPriceSQLStatement);
         ResultSet seatPrice = execStatGetPrice.executeQuery();
         seatPrice.next();

         int seatCost = seatPrice.getInt(seat_class);

         String bookSQLStatement = "insert into booking (id, pass_id, flight_id, datetime, price, seat_class, price, row, letter) " +
                                    "values (" 
                                    + (maxId + 1) + ", "
                                    + pass_id + ", "
                                    + flight_id + ", "
                                    + "'" + getCurrentTimeStamp() + "', "
                                    + seatCost + ", "
                                    + newSeatRow + ", "
                                    + "'" + newSeatLetter + "');";
         
         PreparedStatement execStatBookSeat = connection.prepareStatement(bookSQLStatement);
         execStatBookSeat.executeQuery();
      }
      catch(SQLException ex){
         ex.printStackTrace();
      }
   }

   // Add more helper functions below if desired.
   private void upgradeHelper(String newSeatClass, int booking_id) {
      try {
         String seatQuery = "select max(row) max_row, max(letter) max_letter from booking where seat_class = '" +
                          newSeatClass + "';";
         PreparedStatement execStatMaxSeat = connection.prepareStatement(seatQuery);
         ResultSet maxSeat = execStatMaxSeat.executeQuery();
         maxSeat.next();
         
         int maxSeatRow = maxSeat.getInt("max_row");
         String maxSeatLetter = maxSeat.getString("max_letter");

         int newSeatRow;
         String newSeatLetter;
         if(maxSeatLetter.equals("F")){
            newSeatRow = maxSeatRow + 1;
            newSeatLetter = "A";
         }else{
            newSeatRow = maxSeatRow;
            newSeatLetter = seatLetters.get(seatLetters.indexOf(maxSeatLetter) + 1);
         }
         
         String upgradeSQLStatement = "update booking set row = " + newSeatRow +
               ", letter = '" + newSeatLetter +
               "' booking_time = " + getCurrentTimeStamp() + " where seat_class = '" + newSeatClass +
               "' where id = " + booking_id;


         PreparedStatement execStatUpgrade = connection.prepareStatement(upgradeSQLStatement);
         execStatUpgrade.executeQuery();

      } catch (SQLException ex) {
         ex.printStackTrace();
      }

   }

   /* ----------------------- Main method below ------------------------- */

   public static void main(String[] args) {
      // You can put testing code in here. It will not affect our autotester.
      try {
         Assignment2 test = new Assignment2();
         System.out.println("Upgrade result: " + test.upgrade(10));
      } catch (SQLException e) {
         // TODO Auto-generated catch block
         e.printStackTrace();
      }
   }

}
