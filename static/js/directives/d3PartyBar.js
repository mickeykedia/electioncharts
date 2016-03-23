(function(){
  'use strict';
electionChartsApp.directive('d3PartyBar',['$window','$timeout','$compile','d3Service',function($window,$timeout,$compile,d3Service){

        return {
            restrict:'EA',
            scope:{
                data:'=',
                show:'=',
                party:'=',
                results:'='
            },
            link:function(scope,element,attrs){
                d3Service.d3().then(function(d3){
                    var renderTimeout;

                    var margin = {top:40,right:10,bottom:10,left:50};


                    var svg = d3.select(element[0])
                        .append("svg");

                    var notEnoughData = d3.select(element[0]).select("#ned");

                    var loading = d3.select("#loading");

                    var numberFormat =  function (x) {
                        return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                    };
                    scope.$watch('data',function(newVals,oldVals){
                        scope.render(newVals,scope.party,scope.results,scope.show);
                        $compile(element.contents())(scope);
                    },true);
                    scope.$watch('results',function(newVals,oldVals){
                        scope.render(scope.data,scope.party,newVals);
                        $compile(element.contents())(scope);
                    },true);
                    scope.$watch('show',function(newVals,oldVals){
                        scope.render(scope.data,scope.party,scope.results,newVals);
                        $compile(element.contents())(scope);
                    },true);

                    /*
                     watch for show , include it in function below
                     */
                    var colorAlter = function ColorLuminance(hex, lum) {

                        // validate hex string
                        hex = String(hex).replace(/[^0-9a-f]/gi, '');
                        if (hex.length < 6) {
                            hex = hex[0]+hex[0]+hex[1]+hex[1]+hex[2]+hex[2];
                        }
                        lum = lum || 0;

                        // convert to decimal and change luminosity
                        var rgb = "#", c, i;
                        for (i = 0; i < 3; i++) {
                            c = parseInt(hex.substr(i*2,2), 16);
                            c = Math.round(Math.min(Math.max(0, c + (c * lum)), 255)).toString(16);
                            rgb += ("00"+c).substr(c.length);
                        }

                        return rgb;
                    }

                    var notEnoughDataFunction = function(){
                        notEnoughData.style("display","block");
                        loading.style("display","none");
                        svg.attr("height","0");
                    }

                    var loadingDataNow = function(){
                        /**
                         * Actually loading data - so dismiss the alerts now.
                         */
                        notEnoughData.style("display","none");
                        loading.style("display","none");
                    }


                    scope.render = function(data,party,results,show){
                        svg.selectAll('*').remove();


                        /**
                         * going to be used to calculate position of dotted line.
                         * @type {number}
                         */
                        var i = 0;
                        var j = 0;

                        if(!data) return;
                        /**
                         *
                         */
                        if(!show || show=="all"){

                            data = data.declared.concat(data.undeclared);
                            if(data.length < 3) {
                                notEnoughDataFunction();
                                return ;
                            }
                            data.sort(function(a,b){
                                return b.lead - a.lead;
                            });
                            i =results.wins + results.leads;
                            j =data.length-i;
                        }else if(show=="declared"){
                            if(data.declared.length < 3) {
                                notEnoughDataFunction();
                                return ;
                            }else {
                                data = data.declared;
                                i =results.wins;
                                j =data.length-i;
                            }
                        }else if(show=="undeclared"){
                            if(data.undeclared.length < 3) {
                                notEnoughDataFunction();
                                return ;
                            }else {
                                data = data.undeclared;
                                i =results.leads;
                                j =data.length-i;
                            }

                        }
                        loadingDataNow();


                        var height = 400 - margin.top - margin.bottom,
                            width = d3.select(element[0]).node().offsetWidth - margin.left - margin.right,
                            yScale = d3.scale.pow().exponent(0.5)
                                .domain(d3.extent(data,function(d){
                                        return d.lead;
                                }))
                                .range([height,0]).clamp(true),
                            xScale= d3.scale.ordinal()
                                .domain(data.map(function(d){
                                    return d.constituency_id+":"+d.candidate_name;
                                })).rangeBands([0,width],0.15,0.05);


                        var  colour_swing = "#006600",
                            colour ="#4D944D",
                            colourTrail="#7D7D7E",
                            colourTrail_swing="#000000";


                        var min = d3.min(data,function(d){
                            return d.lead;
                        })


                        /**
                         * find the first candidate with a lead, first candidate with a trail and the first candidate.
                         * Figure out the x axis position of those three points and draw lines and write text
                         * on the SVG. Text must count the number of wins/leads and trails as well.
                         * Add (lead %)
                         */


                        svg.attr('height',height + margin.top + margin.bottom)
                            .attr('width',width + margin.left + margin.right)
                            .attr("border",1);


                        var svgG = svg.append("g")
                            .attr("transform","translate("+margin.left+","+margin.top+")");

                        var yAxis = d3.svg.axis()
                            .scale(yScale)
                            .orient("left");

                        svgG.selectAll('.bar')
                            .data(data.sort(function(a,b){
                                return b.lead - a.lead;
                            }))
                            .enter()
                            .append('rect')
                            .attr("class",function(d){
                                return "bar";
                            })
                            .attr('width',xScale.rangeBand())
                            .attr('y',function(d){
                                return yScale(Math.max(0, d.lead));
                            })
                            .attr('x',function(d){
                                return xScale(d.constituency_id+":"+d.candidate_name);
                            })
                            .attr('fill',function(d){
                                if(d.status=="TRAIL" || d.status=="LOST"){
                                    if(d.party_id == d.last_time_party_id){
                                        return colourTrail_swing;
                                    }else {
                                        return colourTrail;
                                    }
                                }else {
                                    if(d.party_id != d.last_time_party_id){

                                        return colour_swing;
                                    }else {
                                        return colour;

                                    }
                                }
                            })
                            .attr('title',function(d){
                                var str = d.constituency_name+" ("+d.status+")";
                                if(d.party_id == d.last_time_party_id){
                                    if(d.status =="TRAIL" || d.status =="LOST"){
                                        str=str+"  | <b>SWING SEAT</b><br/>";
                                    }
                                }else {
                                    if(d.status =="WIN" || d.status =="LEAD"){
                                        str=str+"  | <b>SWING SEAT</b><br/>";
                                    }
                                }
                                return str;
                            })
                            .attr('my-popover',function(d){
                                var str = "Candidate : "+ d.candidate_name+"<br/>";
                                /**
                                 * Put commas in the numbers,
                                 * difficult to read them or else.
                                 * @type {string}
                                 */
                                if(d.status=="TRAIL"){
                                    str = str+"Trail by: "+(-d.lead).toString()+"<br/>";
                                    str = str+"Total Votes : "+ d.votes+"<br/>";
                                    str = str+"Winning Party: "+ d.winning_party_name+"<br/>";
                                }else if (d.status=="LEAD"){
                                    str = str+"Lead by : "+ d.lead.toString()+"<br/>";
                                    str = str+"Total Votes : "+ d.votes+"<br/>";
                                    str = str+"Runner-up Party: "+ d.loosing_party_name+"<br/>";
                                }else if(d.status=="LOST"){
                                    str=str+"Lost by : "+ (-d.lead).toString()+"<br/>";
                                    str = str+"Total Votes : "+ d.votes+"<br/>";
                                    str = str+"Winning Party: "+ d.winning_party_name+"<br/>";
                                }else {
                                    str = str+"Won by :"+ d.lead.toString()+"<br/>";
                                    str = str+"Total Votes : "+ d.votes+"<br/>";
                                    str = str+"Runner-up Party: "+ d.loosing_party_name+"<br/>";
                                };
                                return str;
                            })
                            .attr('popover-append-to-body',true)
                            .attr('leads',function(d){
                                return d.lead;
                            })
                            .transition()
                            .duration(1000)
                            .attr('height', function (d) {
                                return Math.abs(yScale(d.lead) - yScale(0));
                            });

                        /**
                         * Adding a line to demarcate the trailing/leading line.
                         * also a text which says - constituency in the right place on the graph.
                         */
                        if (i>0 & i < data.length){
                            var trailLineX = xScale(data[i].constituency_id+":"+ data[i].candidate_name);
                            svgG.append("line")
                                .attr("x1",trailLineX)
                                .attr("y1",0)
                                .attr("x2",trailLineX)
                                .attr("y2",height)
                                .attr("stroke","black")
                                .attr("stroke-dasharray","5,5");

                            if(trailLineX < width/4){
                                svgG.append('text')
                                    .attr('x',trailLineX+margin.left)
                                    .attr('y',yScale(0)-margin.top)
                                    .attr('font-style','italic')
                                    .text('Constituency');
                            }else {
                                svgG.append('text')
                                    .attr('x',trailLineX-(2*margin.left+margin.right))
                                    .attr('y',yScale(0)+margin.top)
                                    .attr('font-style','italic')
                                    .text('Constituency');
                            }


                        }

                        /**
                         * adding axes.
                         */

                        svgG.append("g")
                            .attr("class","y axis")
                            .call(yAxis)
                            .append("text")
                            .attr("y",-10)
                            .attr("x",-5)
                            .attr("dy",".71em")
                            .style("text-anchor","end")
                            .style("font-size","0.8em")
                            .text("Margin");

                        svgG.append("g")
                            .attr("class","x axis")
                            .append("line")
                            .attr("y1",yScale(0))
                            .attr("y2",yScale(0))
                            .attr("x2",width);

                    }

                });

            }

        };

    }]);
}());