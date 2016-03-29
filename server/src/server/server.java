package server;

public class server {
	
	public static void main(String[] args) {	     
		 
		Thread relda = new watchRelda();
		relda.setName("relda");

		relda.start();
	}  
	 
}