
public class MethodPrinter {

  /**
	 * @param args
	 */
	public static void main(String[] args) {
		printMethod();
	}
	
	public static void printMethod(){
		try {
			throw new Exception();
		} catch(Exception e) {
			System.out.println(e.getStackTrace()[1].getMethodName());
		}
	}
	
}
