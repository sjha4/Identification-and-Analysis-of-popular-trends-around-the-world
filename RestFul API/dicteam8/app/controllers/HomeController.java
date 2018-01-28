package controllers;

import play.libs.Json;
import play.mvc.*;

import com.amazonaws.services.dynamodbv2.AmazonDynamoDB;
import com.amazonaws.services.dynamodbv2.AmazonDynamoDBClientBuilder;
import com.amazonaws.services.dynamodbv2.model.AttributeDefinition;
import com.amazonaws.services.dynamodbv2.model.AttributeValue;
import com.amazonaws.services.dynamodbv2.model.ProvisionedThroughputDescription;
import com.amazonaws.services.dynamodbv2.model.QueryRequest;
import com.amazonaws.services.dynamodbv2.model.QueryResult;
import com.amazonaws.services.dynamodbv2.model.ScanRequest;
import com.amazonaws.services.dynamodbv2.model.ScanResult;
import com.amazonaws.services.dynamodbv2.model.TableDescription;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.TreeMap;

import com.amazonaws.AmazonServiceException;
import com.amazonaws.auth.AWSStaticCredentialsProvider;
import com.amazonaws.auth.BasicAWSCredentials;
import com.amazonaws.regions.Regions;


/**
 * This controller contains an action to handle HTTP requests
 * to the application's home page.
 */
public class HomeController extends Controller {

    /**
     * An action that renders an HTML page with a welcome message.
     * The configuration in the <code>routes</code> file means that
     * this method will be called when the application receives a
     * <code>GET</code> request with a path of <code>/</code>.
     */
	BasicAWSCredentials awsCreds = new BasicAWSCredentials("AKIAIUXWPXCNXXZQKZQA", "BJCYwL5zAEIt3hPGZnfkt3RBU1SAYgjQRlKqGzfX");
	AmazonDynamoDB ddb = AmazonDynamoDBClientBuilder.standard()
			.withCredentials(new AWSStaticCredentialsProvider(awsCreds))
			.withRegion(Regions.US_EAST_1)
			.build();
	String table_name = "live_twitter_dic8";
    public Result index() {
    	int countRecords =0;
    	int countReplies = 0;
    	Map<String,Integer> keywordCount = new HashMap<>();
    	try {
//    	    TableDescription table_info =
//    	       ddb.describeTable(table_name).getTable();
    	    ScanRequest scanRequest = new ScanRequest()
                    .withTableName(table_name);
    	    Map<String,AttributeValue> lastKey = null;
    	    
            do {
            	
                ScanResult scanResult = ddb.scan(scanRequest);
     
                List<Map<String,AttributeValue>> results = scanResult.getItems();
                countRecords+=results.size();
                results.forEach(r->{
                	System.out.println(r);
                	});
                System.out.println("Count Records: "+countRecords);
                for(Map<String,AttributeValue> mp : results){
                	//for(String s:mp.keySet()){
                		try{
                			countReplies = mp.get("replies").getN()==null?-99:Integer.parseInt(mp.get("replies").getN());
                		}
                		catch(Exception e){
                			countReplies = -99;
                		}
                		if(keywordCount.containsKey(mp.get("key_word"))){
                			keywordCount.put(mp.get("key_word").getS(), keywordCount.get(mp.get("key_word"))+ countReplies);
                		}
                		else{
                			keywordCount.put(mp.get("key_word").getS(),countReplies);
                		}
                	//}
                }
                //results.forEach(r->System.out.println(r.get("key_word").getS()));
                lastKey = scanResult.getLastEvaluatedKey();
                scanRequest.setExclusiveStartKey(lastKey);
            } while (lastKey!=null);
    	} catch (AmazonServiceException e) {
    	    System.err.println(e.getErrorMessage());
    	    System.exit(1);
    	}
    	System.out.println("----------------------Scanned Results-------------------------");
    	for(String s:keywordCount.keySet()){
    		System.out.println(s+" : " + keywordCount.get(s));
    	}
        return ok(views.html.index.render());
    }
    public Result hourly() {
    	ObjectNode responseJson = Json.newObject();
    	ArrayNode responseArray = Json.newArray();
    	String keyword ="";
    	DateFormat dateHourFormat = new SimpleDateFormat("yyyy-MM-dd-HH");
    	DateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
    	Date date = new Date();
    	String hour = dateHourFormat.format(date);
    	String starthour = dateFormat.format(date)+"-00";
    	Map<String,Integer> keywordCount = new HashMap<>();
    	try{
    		Map<String,String> expressionAttributesNames = new HashMap<>();
    	    expressionAttributesNames.put("#key_datetime","key_datetime");
    	    Map<String,AttributeValue> expressionAttributeValues = new HashMap<>();
    	    expressionAttributeValues.put(":from",new AttributeValue().withS(starthour));
    	    expressionAttributeValues.put(":to",new AttributeValue().withS(hour));
    		ScanRequest scanRequest = new ScanRequest()
                .withTableName("combinedTable_hourly")
                .withFilterExpression("#key_datetime BETWEEN :from AND :to ")
    		.withExpressionAttributeNames(expressionAttributesNames)
            .withExpressionAttributeValues(expressionAttributeValues);
	    Map<String,AttributeValue> lastKey = null;
	    int countReplies = 0;
	    do {
        	
            ScanResult scanResult = ddb.scan(scanRequest);
 
            List<Map<String,AttributeValue>> results = scanResult.getItems();
            //int countRecords = results.size();
            results.forEach(r->{
            	System.out.println(r);
            	});
            for(Map<String,AttributeValue> mp : results){
            	keyword = mp.get("key_word").getS().trim().toLowerCase();
            	try{
            		countReplies = mp.get("score").getN()==null?-99:Integer.parseInt(mp.get("score").getN());
        		}
            	catch(Exception e){
        			countReplies = -99;
        		}
            	if(keywordCount.containsKey(keyword)){
        			keywordCount.put(keyword, keywordCount.get(keyword)+ countReplies+1);
        		}
        		else{
        			keywordCount.put(keyword,countReplies+1);
        		}
        	//}
            	
            }
            lastKey = scanResult.getLastEvaluatedKey();
            scanRequest.setExclusiveStartKey(lastKey);
        } while (lastKey!=null);
	} catch (AmazonServiceException e) {
	    System.err.println(e.getErrorMessage());
	    System.exit(1);
	}
//    	Map<String,Integer> keywordCountTop = new HashMap<>();
//    	keywordCountTop = getTop10(keywordCount);
	    int count = 0;
    	for(String s:keywordCount.keySet()){
	    	responseJson = Json.newObject();
	    	responseJson.put("keyword",s);
	    	responseJson.put("count",keywordCount.get(s));
	    	responseArray.add(responseJson);
	    	if(++count==10){
	    		return ok(responseArray);
	    	}
	    }
    	return ok(responseArray);
    }
    private Map<String, Integer> getTop10(Map<String, Integer> keywordCount) {
    	Map<Integer,String> keywordCountTop = new TreeMap<>();
    	Map<String, Integer> returnMap = new HashMap<>();
    	for(Entry<String,Integer> e: keywordCount.entrySet()){
    		int count = e.getValue();
    		while(keywordCountTop.containsKey(count))
    			count++;
    		keywordCountTop.put(count, e.getKey());
    	}
    	int top = 10;
    	for(int x:keywordCountTop.keySet()){
    		top++;
    		returnMap.put(keywordCountTop.get(x), x);
    		if(top==10)
    			return returnMap;
    	}
    	return returnMap;
	}
	public Result minute() {
    	ObjectNode responseJson = Json.newObject();
    	ArrayNode responseArray = Json.newArray();
    	String keyword = "";
    	Map<String,Integer> keywordCount = new HashMap<>();
    	try{
    		ScanRequest scanRequest = new ScanRequest()
                    .withTableName("combinedTable");
	    Map<String,AttributeValue> lastKey = null;
	    int countReplies = 0;
	    do {
        	
            ScanResult scanResult = ddb.scan(scanRequest);
 
            List<Map<String,AttributeValue>> results = scanResult.getItems();
            //int countRecords = results.size();
            results.forEach(r->{
            	System.out.println(r);
            	});
            for(Map<String,AttributeValue> mp : results){
            	keyword = mp.get("key_word").getS().trim().toLowerCase();
            	try{
            		countReplies = mp.get("score").getN()==null?-99:Integer.parseInt(mp.get("score").getN());
            		if(countReplies==0){
            			countReplies=1;
            		}
        		}
            	catch(Exception e){
        			countReplies = -99;
        		}
            	if(keywordCount.containsKey(keyword)){
        			keywordCount.put(keyword, keywordCount.get(keyword)+ countReplies+1);
        		}
        		else{
        			keywordCount.put(keyword,countReplies+1);
        		}
        	//}
            	
            }
            lastKey = scanResult.getLastEvaluatedKey();
            scanRequest.setExclusiveStartKey(lastKey);
        } while (lastKey!=null);
	} catch (AmazonServiceException e) {
	    System.err.println(e.getErrorMessage());
	    System.exit(1);
	}
    	
		for(String s:keywordCount.keySet()){
	    	responseJson = Json.newObject();
	    	responseJson.put("keyword",s);
	    	responseJson.put("count",keywordCount.get(s));
	    	responseArray.add(responseJson);
	    }
    	return ok(responseArray);

    }
    public Result realTime(){
    	ObjectNode responseJson = Json.newObject();
    	ArrayNode responseArray = Json.newArray();
    	DateFormat dateHourFormat = new SimpleDateFormat("yyyy-MM-dd-HH");
    	DateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
    	Date date = new Date();
    	String hour = dateHourFormat.format(date);
    	String starthour = dateFormat.format(date)+"-00";
    	System.out.println(hour);
    	System.out.println(starthour);
    	//2016/11/16 12:08:43
    	Map<String,Integer> keywordCount = new HashMap<>();
    	String keyword = "";
    	try{
    		Map<String,String> expressionAttributesNames = new HashMap<>();
    	    expressionAttributesNames.put("#key_datetime","key_datetime");
    	    Map<String,AttributeValue> expressionAttributeValues = new HashMap<>();
    	    expressionAttributeValues.put(":from",new AttributeValue().withS(starthour));
    	    expressionAttributeValues.put(":to",new AttributeValue().withS(hour));
    		ScanRequest scanRequest = new ScanRequest()
                .withTableName("combinedTable_hourly")
                .withFilterExpression("#key_datetime BETWEEN :from AND :to ")
    		.withExpressionAttributeNames(expressionAttributesNames)
            .withExpressionAttributeValues(expressionAttributeValues);
	    Map<String,AttributeValue> lastKey = null;
	    int countReplies = 0;
	    do {
        	
            ScanResult scanResult = ddb.scan(scanRequest);
 
            List<Map<String,AttributeValue>> results = scanResult.getItems();
            //int countRecords = results.size();
            results.forEach(r->{
            	System.out.println(r);
            	});
            for(Map<String,AttributeValue> mp : results){
            	keyword = mp.get("key_word").getS().trim().toLowerCase();
            	try{
            		countReplies = mp.get("score").getN()==null?-99:Integer.parseInt(mp.get("score").getN());
        		}
            	catch(Exception e){
        			countReplies = -99;
        		}
            	if(keywordCount.containsKey(keyword)){
        			keywordCount.put(keyword, keywordCount.get(keyword)+ countReplies);
        		}
        		else{
        			keywordCount.put(keyword,countReplies);
        		}
        	//}
            	
            }
            lastKey = scanResult.getLastEvaluatedKey();
            scanRequest.setExclusiveStartKey(lastKey);
        } while (lastKey!=null);
	} catch (AmazonServiceException e) {
	    System.err.println(e.getErrorMessage());
	    System.exit(1);
	}
    	try{
    		dateHourFormat = new SimpleDateFormat("yyyy-MM-dd-HH-mm-ss");
        	dateFormat = new SimpleDateFormat("yyyy-MM-dd-HH");
        	//Date date = new Date();
        	hour = dateHourFormat.format(date);
        	starthour = dateFormat.format(date)+"-00-00";
        	System.out.println(hour);
        	System.out.println(starthour);
    		Map<String,String> expressionAttributesNames = new HashMap<>();
    	    expressionAttributesNames.put("#key_datetime","key_datetime");
    	    Map<String,AttributeValue> expressionAttributeValues = new HashMap<>();
    	    expressionAttributeValues.put(":from",new AttributeValue().withS(starthour));
    	    expressionAttributeValues.put(":to",new AttributeValue().withS(hour));
    		ScanRequest scanRequest = new ScanRequest()
                    .withTableName("combinedTable")
                    .withFilterExpression("#key_datetime BETWEEN :from AND :to ")
            		.withExpressionAttributeNames(expressionAttributesNames)
                    .withExpressionAttributeValues(expressionAttributeValues);
	    Map<String,AttributeValue> lastKey = null;
	    int countReplies = 0;
	    do {
        	
            ScanResult scanResult = ddb.scan(scanRequest);
 
            List<Map<String,AttributeValue>> results = scanResult.getItems();
            //int countRecords = results.size();
            results.forEach(r->{
            	System.out.println(r);
            	});
            for(Map<String,AttributeValue> mp : results){
            	keyword = mp.get("key_word").getS().trim().toLowerCase();
            	try{
            		countReplies = mp.get("score").getN()==null?-99:Integer.parseInt(mp.get("score").getN());
            		if(countReplies==0){
            			countReplies=1;
            		}
        		}
            	catch(Exception e){
        			countReplies = -99;
        		}
            	if(keywordCount.containsKey(keyword)){
            		
        			keywordCount.put(keyword, keywordCount.get(keyword)+ countReplies);
        		}
        		else{
        			
        			keywordCount.put(keyword,countReplies);
        		}
        	//}
            	
            }
            lastKey = scanResult.getLastEvaluatedKey();
            scanRequest.setExclusiveStartKey(lastKey);
        } while (lastKey!=null);
	} catch (AmazonServiceException e) {
	    System.err.println(e.getErrorMessage());
	    System.exit(1);
	}
    	for(String s:keywordCount.keySet()){
	    	responseJson = Json.newObject();
	    	responseJson.put("keyword",s);
	    	responseJson.put("count",keywordCount.get(s));
	    	responseArray.add(responseJson);
	    }
    	return ok(responseArray);

    	
    }
    public Result checkTopTrends(String keyword){
    	ObjectNode responseJson = Json.newObject();
    	ArrayNode responseArray = Json.newArray();
//    	DateFormat dateHourFormat = new SimpleDateFormat("yyyy-MM-dd-HH");
//    	DateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
//    	Date date = new Date();
//    	String hour = dateHourFormat.format(date);
//    	String starthour = dateFormat.format(date)+"-00";
//    	System.out.println(hour);
//    	System.out.println(starthour);
    	//2016/11/16 12:08:43
    	Map<String,Integer> keywordCount = new HashMap<>();
    	System.out.println(keyword);
    	//String keyword = "";
    	try{
    		DateFormat dateHourFormat = new SimpleDateFormat("yyyy-MM-dd-HH-mm-ss");
    		DateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd-HH");
        	Date date = new Date();
        	String hour = dateHourFormat.format(date);
        	String starthour = dateFormat.format(date)+"-00-00";
        	System.out.println(hour);
        	System.out.println(starthour);
    		
    		Map<String,String> expressionAttributesNames = new HashMap<>();
    	    expressionAttributesNames.put("#key_word","key_word");
    	    expressionAttributesNames.put("#key_datetime","key_datetime");
    	 
    	    Map<String,AttributeValue> expressionAttributeValues = new HashMap<>();
    	    expressionAttributeValues.put(":key_wordValue",new AttributeValue().withS(keyword));
    	    expressionAttributeValues.put(":from",new AttributeValue().withS(starthour));
    	    expressionAttributeValues.put(":to",new AttributeValue().withS(hour));
    	 
    	    QueryRequest queryRequest = new QueryRequest()
                .withTableName("combinedTable")
                .withKeyConditionExpression("#key_word = :key_wordValue and #key_datetime BETWEEN :from AND :to")
                .withExpressionAttributeNames(expressionAttributesNames)
                .withExpressionAttributeValues(expressionAttributeValues);
	    Map<String,AttributeValue> lastKey = null;
	    int countReplies = 0;
	    do {
        	
	    	QueryResult scanResult= ddb.query(queryRequest);
 
            List<Map<String,AttributeValue>> results = scanResult.getItems();
            System.out.println("Size of results"+ results.size());
            //int countRecords = results.size();
            results.forEach(r->{
            	System.out.println(r);
            	});
            for(Map<String,AttributeValue> mp : results){
            	keyword = mp.get("key_datetime").getS();
            	try{
            		countReplies = mp.get("score").getN()==null?-99:Integer.parseInt(mp.get("score").getN());
        		}
            	catch(Exception e){
        			countReplies = -99;
        		}
            	if(keywordCount.containsKey(keyword)){
        			keywordCount.put(keyword, keywordCount.get(keyword)+ countReplies+1);//Add a score for tweet itself
        		}
        		else{
        			keywordCount.put(keyword,countReplies+1);
        		}
        	//}
            	
            }
            lastKey = scanResult.getLastEvaluatedKey();
            queryRequest.setExclusiveStartKey(lastKey);
        } while (lastKey!=null);
	} catch (AmazonServiceException e) {
	    System.err.println(e.getErrorMessage());
	    System.exit(1);
	}
    	for(String s:keywordCount.keySet()){
	    	responseJson = Json.newObject();
	    	responseJson.put("keyword",s.substring(14));
	    	responseJson.put("count",keywordCount.get(s));
	    	responseArray.add(responseJson);
	    }
    	return ok(responseArray);	
    }
    public Result getMeetupsForKeywordMonth(String keyword){
    	ObjectNode responseJson = Json.newObject();
    	ArrayNode responseArray = Json.newArray();
    	try{
        	DateFormat dateHourFormat = new SimpleDateFormat("yyyy-MM-dd-HH");
        	DateFormat dateFormat = new SimpleDateFormat("yyyy-MM");
        	Date date = new Date();
        	String hour = dateHourFormat.format(date);
        	String starthour = dateFormat.format(date)+"-01-00";
    		Map<String,String> expressionAttributesNames = new HashMap<>();
    	    expressionAttributesNames.put("#key_word","key_word");
    	    //Map<String,String> expressionAttributesNames = new HashMap<>();
    	    expressionAttributesNames.put("#key_datetime","key_datetime");
    	    Map<String,AttributeValue> expressionAttributeValues = new HashMap<>();
    	    expressionAttributeValues.put(":from",new AttributeValue().withS(starthour));
    	    expressionAttributeValues.put(":to",new AttributeValue().withS(hour));
    	    //Map<String,AttributeValue> expressionAttributeValues = new HashMap<>();
    	    expressionAttributeValues.put(":key_wordValue",new AttributeValue().withS(keyword));
    	 
    	    QueryRequest queryRequest = new QueryRequest()
                .withTableName("meetups_dic8")
                .withKeyConditionExpression("#key_word = :key_wordValue and #key_datetime BETWEEN :from AND :to")
                .withExpressionAttributeNames(expressionAttributesNames)
                .withExpressionAttributeValues(expressionAttributeValues);
	    Map<String,AttributeValue> lastKey = null;
	    int countReplies = 0;
	    do {
        	
	    	QueryResult scanResult= ddb.query(queryRequest);
 
            List<Map<String,AttributeValue>> results = scanResult.getItems();
            System.out.println("Size of results"+ results.size());
            //int countRecords = results.size();
            results.forEach(r->{
            	System.out.println(r);
            	});
            for(Map<String,AttributeValue> mp : results){
            	keyword = mp.get("key_word").getS().trim().toLowerCase();
            	responseJson = Json.newObject();
            	responseJson.put("key_word",keyword);
            	responseJson.put("key_location_state",mp.get("key_word").getS().trim().toLowerCase());
            	responseJson.put("venue",mp.get("venue").getS().trim().toLowerCase());
            	responseJson.put("key_location_city",mp.get("key_location_city").getS().trim().toLowerCase());
            	responseJson.put("key_category",mp.get("key_category").getS().trim().toLowerCase());
            	responseJson.put("key_location_country",mp.get("key_location_country").getS().trim().toLowerCase());
            	responseJson.put("name",mp.get("name").getS().trim().toLowerCase());
            	responseJson.put("key_datetime",mp.get("key_datetime").getS().trim().toLowerCase());
            	responseArray.add(responseJson);
            	
        	}
//            	
//            }
            lastKey = scanResult.getLastEvaluatedKey();
            queryRequest.setExclusiveStartKey(lastKey);
        } while (lastKey!=null);
	} catch (AmazonServiceException e) {
	    System.err.println(e.getErrorMessage());
	    System.exit(1);
	}
    	return ok(responseArray);
    }
    
}
