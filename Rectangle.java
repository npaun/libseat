import java.util.*;

public class Rectangle{
  String name;
  double prob;
  double tlx; //topLeftX
  double tly; //topLeftY
  double brx; //bottomRightX
  double bry; //bottomRightY
  
  public Rectangle(double tlx, double tly, double brx, double bry){
    this.tlx = tlx;
    this.tly = tly;
    this.brx = brx;
    this.bry = bry;
  }
  
  public void setProb(double prob){
    this.prob = prob;
  }
  
  public double getProb(){
    return this.prob;
  }
  
  public void setName(String name){
    this.name = name;
  }
  
  public String getName(){
    return this.name;
  }
  
  public double area(){
    double length = Math.abs(brx - tlx);
    double width = Math.abs(tly - bry);
    return length*width;
  }
  
  public double getTLX(){
    return this.tlx;
  }
  
  public double getTLY(){
    return this.tly;
  }
  
  public double getBRX(){
    return this.brx;
  }
  
  public double getBRY(){
    return this.bry;
  }
  
  public double getBLX(){
    return this.tlx;
  }
  
  public double getBLY(){
    return this.tly;
  }
  
  public double getTRX(){
    return this.brx;
  }
  
  public double getTRY(){
    return this.bry;
  }
  
  
  
  
  
  
}