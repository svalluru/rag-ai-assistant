/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package com.sales;


import java.util.Map;
import java.util.Random;

import org.apache.camel.Exchange;
import org.apache.camel.Processor;
import org.apache.camel.ProducerTemplate;
import org.apache.camel.builder.RouteBuilder;

public class CopyDBData2Kafka extends RouteBuilder {
    @Override
    public void configure() throws Exception {

        //from("kafka:customerdata").log("${body}");

        from("timer://insertCamel?period={{timer.period}}").noAutoStartup()
                .setBody().simple("SELECT * FROM customerdata")
                .to("jdbc:source_db")
                //.log("${body}")
                .split(body())
                .process( new Processor() {

                    @Override
                    public void process(Exchange exchange) throws Exception {
                        // TODO Auto-generated method stub
                        Map<String, Object> sourceData = exchange.getIn().getBody(Map.class);
                        //System.out.println(sourceData.keySet());
                        Random rand = new Random();                        
                        //int rand_int1 = rand.nextInt(2000);
                        String msg = "An Order "+sourceData.get("Order ID") + " was created by "+ 
                        sourceData.get("Contact Name") + " for Product "+ sourceData.get("Product")+ " in Region " + sourceData.get("Region") + " and Country " + 
                        sourceData.get("Country")+ " using Customer ID " + sourceData.get("Customer ID"); 
                        ProducerTemplate template = exchange.getContext().createProducerTemplate();                        
                        //System.out.println(msg);
                        //exchange.getIn().setBody("test");
                        template.sendBody("direct:send2kafka",msg);
                    }                    
                });
                
                from("direct:send2kafka").to("kafka:customerdata");//?brokers=localhost:9092");//.log("done");
            ;
                    
    }
}
