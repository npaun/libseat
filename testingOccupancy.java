import java.util.*;
import java.io.*;

public class testingOccupancy{
  public static void main(String args[]){
    getBool x = new getBool();
    HashMap<String,Boolean> h = new HashMap<String,Boolean>();
    try{
     h = x.occupancy("testVal1.txt","testVal.txt");
    } catch (IOException e){
    }
    System.out.println(h);
  }
}