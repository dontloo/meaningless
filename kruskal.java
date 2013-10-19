import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;


public class mst {
	
	private static double[][] graph;
	private static double[] weight;
	private static int[] from;
	private static int[] to;
	private static int[] parent;
	private static int[] rank;
	private static List<Integer> mstIndices;
	
	public static void generateGraph(int size){
		graph = new double[size][size];
		for(int i=0; i<size; i++){
			for(int j=0; j<=i; j++){
				graph[i][j] = Math.random();
				graph[j][i] = graph[i][j];
			}
		}
		extractEdges();
	}
	
	public static void extractEdges(){
		weight = new double[((graph.length)*(graph.length)-graph.length)/2];
		from = new int[weight.length];
		to = new int[weight.length];
		int pos = 0;
		for(int i=0; i<graph.length; i++){
			for(int j=0; j<i; j++){
				weight[pos] = graph[i][j];
				from[pos] = i;
				to[pos] = j;
				pos++;
			}
		}
	}
	
	public static void sortEdges(int left, int right){
		if (left<right){
			int pi = partition(left,right);
			sortEdges(left,pi-1);
			sortEdges(pi+1,right);
		}
	}
	
	public static int partition(int left, int right){
		int p = left+(int)(Math.random()*(right-left));
		swapEdge(p,right);
		int store = left;
		for(int i=left; i<right; i++){
			if(weight[i]<=weight[right]){
				swapEdge(i,store);
				store++;
			}
		}
		swapEdge(store,right);
		return store;
	}
	
	public static void swapEdge(int e1, int e2){
		double w = weight[e1];
		int f = from[e1];
		int t = to[e1];
		weight[e1] = weight[e2];
		from[e1] = from[e2];
		to[e1] = to[e2];
		weight[e2] = w;
		from[e2] = f;
		to[e2] = t;
	}
	
	public static void initSet(int size){
		parent = new int[size];
		rank = new int[size];
	}
	
	public static void makeSet(int x){
		parent[x] = x;
		rank[x] = 0;
	}
	
	public static void union(int x, int y){
		link(findSet(x),findSet(y));
	}
	
	public static void link(int x, int y){
		if(rank[x]>rank[y]){
			parent[y] = x;
		}else{
			parent[x] = y;
			if(rank[x] == rank[y])
				rank[y] += 1;
		}
	}
	
	public static int findSet(int x){
		if(parent[x]!=x)
			parent[x] = findSet(parent[x]);
		return parent[x];
	}
	
	public static void kruskal(){
		mstIndices = new ArrayList<Integer>(graph.length-1);
		initSet(graph.length);
		for(int i=0; i<graph.length; i++)
			makeSet(i);
		sortEdges(0, weight.length-1);
		for(int i=0; i<weight.length; i++){
			if(findSet(from[i])!=findSet(to[i])){
				mstIndices.add(i);
				union(from[i],to[i]);
			}
		}
	}
	
	public static double weightSum(){
		double weightSum =0;
		for(Integer idx: mstIndices){
			weightSum += weight[idx];
		}
		return weightSum;
	}
	
	public static void printMst(){
		for(Integer idx: mstIndices){
			System.out.println(from[idx]+" "+to[idx]+" "+weight[idx]);
		}
	}
	
	public static void printGraph(){
		for(int i=0; i<graph.length; i++){
			System.out.println(Arrays.toString(graph[i]));
		}
	}
	
	public static void main(String[] args) {
		int size[] = {10,100,150,200};
		for (int i=0; i<size.length; i++){
			long totalTime = 0;
			double weightSum = 0;
			for(int j=0; j<50; j++){
				generateGraph(size[i]);
				long startTime = System.currentTimeMillis();
				kruskal();
				long endTime = System.currentTimeMillis();
				totalTime += endTime - startTime;
				weightSum+=weightSum();
			}
			System.out.println("Kruskal run in "+ (float)totalTime/50+" milliseconds with weight sum of "+weightSum/50 +" for" +size[i] + " vertices" );
		}
//		printGraph();
//		printMst();
	}

}
