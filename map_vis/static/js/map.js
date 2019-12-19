function map(state, airport, route, airline_route, airline, time_route, state_json) {
    //console.log(state)
    //console.log(airport)
    //console.log(route)
    //console.log(airline_route)
    //console.log(airline)
    //console.log(time_route)
    //console.log(state_json);

    var width = 960;
    var height = 600;
    var width_air = 200;
    var height_air = 480;
    var height_time = 40
    var width_time = 800

    var proj = d3.geo.albersUsa()
                 .translate([width/2, height/2])
                 .scale(1000);

    var map_svg = d3.select("body")
                    .append("svg")
                    .attr("width", width)
                    .attr("height", height)
                    .append("g");

    var air_svg = d3.select("body")
                    .append("svg")
                    .attr("width", width_air)
                    .attr("height", height_air)
                    .append("g")
                    .attr("transform", "translate(" + 0 + "," + 0 + ")");

    var time_svg = d3.select("body")
                    .append("svg")
                    .attr("width", width)
                    .attr("height", height_time)
                    .append("g")
                    .attr("transform", "translate(" + 0 + "," + 0 + ")");

    var path = d3.geo.path()
                .projection(proj);

    var div = d3.select("body")
                .append("div")
                .attr("class", "tooltip")
                .style("opacity", 0);

    // Plot The states by color
    var color_start = d3.rgb(255,255,255);
    var color_end = d3.rgb(0,0,128);
    var compColor = d3.interpolate(color_start, color_end);
    var max_state_count = state["Max_Count"];
    var rescale_state_count = d3.scale.linear().domain([0, max_state_count]).range([0.2, 0.8]);

    map_svg.selectAll("path")
       .data(state_json.features)
       .enter()
       .append("path")
       .attr("d", path)
       .style("fill", function(d) {
           if (d.properties.name in state) {
               return compColor(rescale_state_count(state[d.properties.name].Count));
           }
       })
       // Mouse over to show the detail count in the year
       .on("mouseover", function(d) {
           div.style("display", "inline");
       })
       .on("mousemove", function(d) {
           div.transition()
              .duration(10)
              .style("opacity", 0.8);

           div.text(function(t) {
               if (d.properties.name in state) {
                   let s = state[d.properties.name]
                   let res = d.properties.name + "\n" + s.State_Abv + "\n" + s.Count
                   return res;
               }
           })
              .style("left", (d3.event.pageX+10) + "px")
              .style("top",  (d3.event.pageY-40) + "px")
              .style("height", 40 + "px")
              .style("width",  80 + "px");
       })
       .on("mouseout", function(d) {
           div.transition()
              .duration(200)
              .style("opacity", 0);
       })

    // Plot the cities in circle by volume
    map_svg.selectAll("circle")
       .data(airport)
       .enter()
       .append("circle")
       .attr("cx", function(d) {
           let loc = proj([d.Longitude, d.Latitude])
           if (loc) {
               return proj([d.Longitude, d.Latitude])[0];
           }
       })
       .attr("cy", function(d) {
           let loc = proj([d.Longitude, d.Latitude])
           if (loc) {
               return proj([d.Longitude, d.Latitude])[1];
           }
       })
       .attr("r", function(d) {
           return Math.sqrt(d.Count)/35;
       })
       .style("fill", "rgb(230,20,145)")
       .style("opacity", 0.9)
       // Mouse over to show the detail count in the year
       .on("mouseover", function(d) {
           div.style("display", "inline");

           map_svg.selectAll("line")
			  .data(route[d.Code]["Destination"])
			  .enter()
			  .append("line")
			  .style("stroke","#cc3366")
			  .style("stroke-width", function(d) {return 5*d.Count / d.Max_Count;})
              .attr("x1", function(d) {return proj([d.Ori_Longitude, d.Ori_Latitude])[0];})
			  .attr("y1", function(d) {return proj([d.Ori_Longitude, d.Ori_Latitude])[1];})
    		  .attr("x2", function(d) {return proj([d.Des_Longitude, d.Des_Latitude])[0];})
    		  .attr("y2", function(d) {return proj([d.Des_Longitude, d.Des_Latitude])[1];});
       })
       .on("mousemove", function(d) {
           div.transition()
              .duration(10)
              .style("opacity", 0.8);

           div.text(d.Name + "(" + d.Code + ")\n" + d.City + "\n" + d.Count)
              .style("left", (d3.event.pageX+10) + "px")
              .style("top",  (d3.event.pageY-40) + "px")
              .style("height", 55 + "px")
              .style("width",  160 + "px")
       })
       .on("mouseout", function(d) {
           div.transition()
              .duration(200)
              .style("opacity", 0);
           map_svg.selectAll("line").remove();
       })

       // For the rectangle with airline. Mouseover it to show flight of this airline
       var padding = 5
       var rec_height = height_air/airline.length;
       rects = air_svg.selectAll("rect")
                      .data(airline)
                      .enter()

       rects.append("rect")
            .attr('width', width_air)
            .attr('height', rec_height-padding)
            .attr('x', 0)
            .attr('y', 0)
            .attr('rx', 10)
            .attr('ry', 10)
            .style('fill', '#9999ff')
            .style('stroke', 'black')
            .style('stroke-width', 0.3)
            .style('opacity', 0.3)
            .attr("transform", function(d,i) {return "translate(" + 0 + "," + i*rec_height + ")";})
            .on("mousemove", function(d) {
                d3.select(this).style("opacity", 0.6);
            })
            .on("mouseover", function(d) {
                  map_svg.selectAll("line")
       			  .data(airline_route[d.Code]["Routes"])
       			  .enter()
       			  .append("line")
       			  .style("stroke","#cc3300")
       			  .style("stroke-width", function(d) {return 5*d.Count / d.Max_Count;})
                  .attr("x1", function(d) {return proj([d.Ori_Longitude, d.Ori_Latitude])[0];})
       			  .attr("y1", function(d) {return proj([d.Ori_Longitude, d.Ori_Latitude])[1];})
           		  .attr("x2", function(d) {return proj([d.Des_Longitude, d.Des_Latitude])[0];})
           		  .attr("y2", function(d) {return proj([d.Des_Longitude, d.Des_Latitude])[1];});
              })
            .on("mouseout", function(d) {
                d3.select(this).style("opacity", 0.3);
                map_svg.selectAll("line").remove();
            });

       rects.append("text").text(function (d) {return d.Name;})
            .attr("x", 0)
            .attr("y", 0)
            .attr("transform", function(d,i) {return "translate(" + 8 + "," + ((i+1)*rec_height-padding-7) + ")";});

       // Time axis
       var start_x = 100
       var blank = 15
       time_axis = time_svg.append("rect")
                           .attr('width', width_time )
                           .attr('height', height_time-blank)
                           .attr('x', start_x)
                           .attr('y', 0)
                           .attr('rx', 10)
                           .attr('ry', 10)
                           .style('fill', '#cc99ff')
                           .style('stroke', 'black')
                           .style('stroke-width', 0);

       // Mouse effect when move mouse to some time point. Show current on air routes
       function pos_to_time(pos, width) {
           let scale_min = Math.floor(pos/width * 24 * 60 - 15); // Actually I do not know when there is always an extra 15-min
           let real_hour = Math.floor(scale_min / 60);
           let real_min = scale_min % 60;
           return 100*real_hour+real_min;
       }
       function filter_by_time(data, time) {
           return data.filter(function (d) {return d.Dep_Time<=time && d.Arr_Time>=time;});
       }
       time_axis.on("mouseover", function(d) {
                     let t = pos_to_time(d3.event.pageX-start_x,width_time)
                     map_svg.selectAll("line")
                     .data(filter_by_time(time_route, t))
                     .enter()
                     .append("line")
                     .style("stroke","#cc3300")
                     .style("stroke-width", 1)
                     .attr("x1", function(d) {return proj([d.Ori_Longitude, d.Ori_Latitude])[0];})
                     .attr("y1", function(d) {return proj([d.Ori_Longitude, d.Ori_Latitude])[1];})
                     .attr("x2", function(d) {return proj([d.Des_Longitude, d.Des_Latitude])[0];})
                     .attr("y2", function(d) {return proj([d.Des_Longitude, d.Des_Latitude])[1];});
                  })
                 .on("mouseout", function(d) {
                     map_svg.selectAll("line").remove();
                 });

       var hours = [...Array(25).keys()];
       var width_hour = width_time / (hours.length-1)
       hour_text = time_svg.selectAll("text").data(hours).enter().append("text")
                           .text(function (d) {return d;})
                           .attr("x", start_x)
                           .attr("y", height_time)
                           .attr("transform", function(d,i) {return "translate(" + i*width_hour + "," + 0 + ")";});
       var line_h = 10
       hour_line = time_svg.selectAll("line").data(hours).enter().append("line")
                           .attr("x1", start_x)
                           .attr("y1", height_time-blank-line_h)
                           .attr("x2", start_x)
                           .attr("y2", height_time-blank)
                           .style('stroke', 'black')
                           .style('stroke-width', 1)
                           .attr("transform", function(d,i) {return "translate(" + i*width_hour + "," + 0 + ")";});

}
