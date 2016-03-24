package client;

public class client {

	public static void main(String args[]) {
		Thread relda = new watchRelda();
		relda.setName("relda");
		Thread reldaResult = new watchReldaResult();
		relda.setName("reldaResult");
		
		relda.start();
		reldaResult.start();		
	}
 
}