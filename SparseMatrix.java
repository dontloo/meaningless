/**
 * @author Donglu Wang
 *
 * This program will compute the transitive closure as follows
 *
 * parameters: 
 * 		a given graph G
 *		number of nodes n
 * return: 
 * 		the transitive closure matrix T
 * pseudo code:
 * 		from 1 to log_2(n):
 * 			T = max(T,T*G)
 *
 * which will take O(n^3*log(n)) time,
 * because the time complexity of matrix multiplication is n^3 in our implementation.
 * We can further speed up the process of matrix multiplication by adopting other algorithms.
 */
import java.util.HashMap;
import java.util.Map;

public class SparseMatrix {

	public static void main(String[] args) throws Exception {
		// an example graph is defined as:
		//	0	1	0	0
		//	0	0	0	1
		//	0	0	0	0
		//	1	0	1	0
		//
		// its transitive closure matrix should to be:
		//	1	1	1	1
		//	1	1	1	1
		//	0	0	0	0
		//	1	1	1	1				
		int noOfNodes = 4;
		SparseMatrix G = new SparseMatrix(noOfNodes,noOfNodes);	
		G.setElement(0, 1, 1);
		G.setElement(1, 3, 1);
		G.setElement(1, 3, 1);
		G.setElement(3, 0, 1);
		G.setElement(3, 2, 1);
		System.out.println("input graph:");
		System.out.println(G.toString());
		
		// transitive closure initialized to G
		SparseMatrix T = G;	
		for(int i=0; i<(int)(Math.log(noOfNodes)/Math.log(2)); i++){
			T = max(T,G.multiply(T));
		}
		System.out.println("transitive closure:");
		System.out.println(T.toString());
		
	}
	
	public int m; // no. of rows
	public int n; // no. of columns
	// keys in the outer map is row number
	public Map<Integer,Map<Integer,Element>> rows = new HashMap<Integer,Map<Integer,Element>>();
	// keys in the outer map is column number
	public Map<Integer,Map<Integer,Element>> cols = new HashMap<Integer,Map<Integer,Element>>();

	public SparseMatrix(int argM, int argN){
		m = argM;
		n = argN;
	}
	
	/**
	 * matrix multiplication by definition
	 * return a new matrix c = a*b
	 */
	public SparseMatrix multiply(SparseMatrix arg) throws Exception{
		if(n!=arg.m){
			throw new Exception("matrix dimensions do not agree.");
		}
		SparseMatrix res = new SparseMatrix(m,arg.n);	
		for(Integer rowIdx: rows.keySet()){
			for(Integer colIdx: arg.cols.keySet()){
				res.setElement(rowIdx,colIdx,dotProduct(rows.get(rowIdx),arg.cols.get(colIdx)));
			}
		}			
		return res;		
	}

	/**
	 * bitwise max() operation
	 * return a new matrix c = max(a,b)
	 */
	public static SparseMatrix max(SparseMatrix a, SparseMatrix b) throws Exception{
		if(a.m!=b.m||a.n!=b.n){
			throw new Exception("matrix dimensions do not agree.");
		}
		SparseMatrix res = new SparseMatrix(a.m,a.n);
		// iterate over both a and b,
		// and set c = max(a,b)
		for(Integer rowIdx: a.rows.keySet()){
			for(Integer colIdx: a.rows.get(rowIdx).keySet()){
				res.setElement(rowIdx,colIdx,Math.max(a.getElement(rowIdx, colIdx), b.getElement(rowIdx, colIdx)));
			}
		}		
		for(Integer rowIdx: b.rows.keySet()){
			for(Integer colIdx: b.rows.get(rowIdx).keySet()){				
				res.setElement(rowIdx,colIdx,Math.max(a.getElement(rowIdx, colIdx), b.getElement(rowIdx, colIdx)));
			}
		}
		return res;
	}
	
	/**
	 * only create an element when the value is not zero
	 */
	public void setElement(int m, int n, int val){
		if(val==0)
			return;
		Element node = new Element(val);
		setMap(rows,m,n,node);
		setMap(cols,n,m,node);
	}
	
	/**
	 * default value of null element is zero
	 */
	public int getElement(int m, int n){
		if(rows.containsKey(m)&&rows.get(m).containsKey(n)){
			return rows.get(m).get(n).val;			
		}
		return 0;		
	}
	
	/**
	 * vector dot product
	 * since default value of null element is zero, which has no effect to the result,
	 * we only need to consider the no zero cases.
	 */
	private int dotProduct(Map<Integer,Element> a, Map<Integer,Element> b){
		if(a==null||b==null)
			return 0;
		int res = 0;
		for(Integer rowIdx: a.keySet()){
			if(b.containsKey(rowIdx)){
				res += a.get(rowIdx).val*b.get(rowIdx).val;
			}
		}
		return res;
	}
	
	/**
	 * for creating new maps instance when necessary
	 */
	private void setMap(Map<Integer,Map<Integer,Element>> argMap, int fstKey, int sndKey, Element val){
		if(!argMap.containsKey(fstKey)){
			argMap.put(fstKey, new HashMap<Integer,Element>());
		}
		argMap.get(fstKey).put(sndKey, val);
	}
	
	public String toString(){
		StringBuilder sb = new StringBuilder();
		for(int i=0; i<m; i++){
			for(int j=0; j<n; j++){
				sb.append("\t");
				sb.append(this.getElement(i, j));
			}
			sb.append("\n");
		}
		return sb.toString();
	}
}

/**
 * @author Donglu Wang
 * for the convenience passing and storing the reference of an element,
 * can not do so if we use the built-in Integer class instead.
 */
class Element{
	public int val;
	public Element(int arg){
		val = arg;
	}
}
