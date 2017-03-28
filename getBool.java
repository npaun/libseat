import java.awt.geom.Point2D;
import java.util.ArrayList;
import java.io.*;
import java.util.HashMap;
import java.util.*;

public class getBool{
  
  //method to open file and read coordinates
  private ArrayList<Rectangle> getRectangles(String fileName) throws IOException{
    
    ArrayList<Rectangle> rectangles = new ArrayList<Rectangle>();
    
    try{
      
      FileReader fr = new FileReader(fileName);
      BufferedReader br = new BufferedReader(fr);
      
      String line = br.readLine();
      
      while(line != null){
        
        String[] elements = line.split(" ");
        
        double tlx = Double.parseDouble(elements[1]);
        double tly = Double.parseDouble(elements[2]);
        double brx = Double.parseDouble(elements[3]);
        double bry = Double.parseDouble(elements[4]);
        double probVal = Double.parseDouble(elements[5]);

        Rectangle rec = new Rectangle(tlx,tly,brx,bry);
        
        rec.setName(elements[0]);
        rec.setProb(probVal);
        rectangles.add(rec);
        line = br.readLine();
        
      }
      
        br.close();
        fr.close();
        
        
    } catch(IOException e){
      System.out.println(e.getMessage());
    } catch(NullPointerException nul){
      System.out.println(nul.getMessage());
    }
    
    
    return rectangles;
  }

  
  //method to calculate area of overlap
  private double overlapArea(Rectangle rec1, Rectangle rec2){
    double xOverlap = Math.max(0,Math.min(rec1.getTRX(),rec2.getTRX()) - Math.max(rec1.getTLX(),rec2.getTLX()));
    double yOverlap = Math.max(0,Math.min(rec1.getTLY(),rec2.getTLY()) - Math.max(rec1.getBRY(),rec2.getBRY()));
    return xOverlap * yOverlap;
  }
  
  
  //method to caculate percentage of overlap
  private double overlapPercent(Rectangle seat, double overlapArea){
    double seatArea = seat.area();
    return (overlapArea/seatArea);
  }
  
  //method to determine occupancy
  private boolean isOccupied(Rectangle seat, Rectangle covered){
    double overlapArea = overlapArea(seat,covered);
    System.out.println(covered.getProb()*overlapPercent(seat,overlapArea));
    if(covered.getProb()*overlapPercent(seat,overlapArea) > 0.5)
      return true;
    else
      return false;
  }
  
  
  //method that checks occupancy
  public HashMap<String,Boolean> occupancy(String seatFile, String CVFile) throws IOException{
    
    ArrayList<Rectangle> seats = new ArrayList<Rectangle>();
    ArrayList<Rectangle> cv = new ArrayList<Rectangle>();
    
    try{
      seats = getRectangles(seatFile);
      cv = getRectangles(CVFile);
    } catch(IOException e){
      System.out.println("IOException in occupancy method");
    }
    HashMap<String,Boolean> occ = new HashMap<String,Boolean>();
    
    //initialize HashMap
    for(int k=0; k<seats.size(); k++){
      occ.put(seats.get(k).getName(),false);
    }
    
    for(int i=0; i<seats.size(); i++){
      for(int j=0; j<cv.size(); j++){
        if(isOccupied(seats.get(i),cv.get(j))){
          occ.put(seats.get(i).getName(),!occ.get(seats.get(i).getName()));
          break;
        }
      }
    }
    
    return occ;
  }
}