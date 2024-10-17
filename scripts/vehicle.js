// Load the data
d3.csv("app/static/vehicle.csv").then(data => {
  // Process and filter the data
  const processedData = data.map(d => ({
      year: d['總計'],
      displayYear: d['總計'].replace(/^(\d+)年.*$/, '$1'),
      yearNumber: parseInt(d['總計'].match(/^(\d+)/)[1]),
      car: +d['汽車'].replace(/,/g, ''),
      bus: +d['大客車'].replace(/,/g, ''),
      truck: +d['大貨車'].replace(/,/g, ''),
      privatecar: +d['小客車'].replace(/,/g, ''),
      van: +d['小貨車'].replace(/,/g, ''),
      special: +d['特種車'].replace(/,/g, ''),
      motorcycle: +d['機車'].replace(/,/g, '')
  })).sort((a, b) => {
      if (a.yearNumber > 100 && b.yearNumber < 100) return 1;
      if (a.yearNumber < 100 && b.yearNumber > 100) return -1;
      return a.yearNumber - b.yearNumber;
  });

  const chartContainer = d3.select(".chart-container");
  const containerWidth = chartContainer.node().getBoundingClientRect().width;

  const margin = { top: 80, right: 20, bottom: 70, left: 80 };
  const width = containerWidth - margin.left - margin.right;
  const height = 600 - margin.top - margin.bottom;

  // Create SVG
  const svg = d3.select("#chart")
      .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

  // Define fixed color mapping with default order
  const defaultOrder = ["car", "bus", "truck", "privatecar", "van", "special", "motorcycle"];
  const colorMapping = {
      "car": "#F7F0F5",
      "bus": "#DECBB7",
      "truck": "#B89A8E",
      "privatecar": "#8F857D",
      "van": "#5C5552",
      "special": "#433633",
      "motorcycle": "#1A1614"
  };

  // Create scales
  const x = d3.scaleBand().range([0, width]).padding(0.1);
  const y = d3.scaleLinear().range([height, 0]);

  // Create axes
  const xAxis = svg.append("g")
      .attr("transform", `translate(0,${height})`);
  const yAxis = svg.append("g");

  // Add x-axis label
  svg.append("text")
      .attr("transform", `translate(${width / 2},${height + margin.bottom - 10})`)
      .style("text-anchor", "middle")
      .text("年份");

  // Add y-axis label
  svg.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - margin.left)
      .attr("x", 0 - (height / 2))
      .attr("dy", "1em")
      .style("text-anchor", "middle")
      .text("數量");

  // Create tooltip
  const tooltip = d3.select("body").append("div")
      .attr("class", "tooltip")
      .style("opacity", 0);

  // Helper function to get Chinese labels
  function getChineseLabel(key) {
      const labels = {
          "car": "汽車",
          "bus": "大客車",
          "truck": "大貨車",
          "privatecar": "小客車",
          "van": "小貨車",
          "special": "特種車",
          "motorcycle": "機車"
      };
      return labels[key];
  }

  // Function to update the chart
  function updateChart() {
      // Set domains
      x.domain(processedData.map(d => d.displayYear));
      const maxTotal = d3.max(processedData, d =>
          defaultOrder.reduce((sum, key) => sum + d[key], 0)
      );
      y.domain([0, maxTotal]);

      // Update axes
      xAxis.call(d3.axisBottom(x));
      yAxis.call(d3.axisLeft(y));

      // Stack the data
      const stackedData = d3.stack()
          .keys(defaultOrder)(processedData);

      // Create and update bars
      const bars = svg.selectAll(".bar")
          .data(stackedData)
          .join("g")
          .attr("class", "bar")
          .attr("fill", d => colorMapping[d.key]);

      bars.selectAll("rect")
          .data(d => d)
          .join("rect")
          .attr("x", d => x(d.data.displayYear))
          .attr("y", d => y(d[1]))
          .attr("height", d => y(d[0]) - y(d[1]))
          .attr("width", x.bandwidth());

      // Add interactivity
      bars.selectAll("rect")
          .on("mouseover", function (event, d) {
              const category = d3.select(this.parentNode).datum().key;
              const value = d[1] - d[0];
              tooltip.transition()
                  .duration(200)
                  .style("opacity", .9);
              tooltip.html(`${d.data.displayYear}年<br>${getChineseLabel(category)}: ${value.toLocaleString()}`)
                  .style("left", (event.pageX) + "px")
                  .style("top", (event.pageY - 28) + "px");
          })
          .on("mouseout", function (d) {
              tooltip.transition()
                  .duration(500)
                  .style("opacity", 0);
          });

      // Add legend
      const legendSpacing = 120;
      const legendsPerRow = Math.floor(width / legendSpacing);

      const legend = svg.selectAll(".legend")
          .data(defaultOrder)
          .join("g")
          .attr("class", "legend")
          .attr("transform", (d, i) => `translate(${(i % legendsPerRow) * legendSpacing}, ${Math.floor(i / legendsPerRow) * 20 - margin.top / 2})`);

      legend.selectAll("rect")
          .data(d => [d])
          .join("rect")
          .attr("x", 0)
          .attr("width", 19)
          .attr("height", 19)
          .attr("fill", d => colorMapping[d]);

      legend.selectAll("text")
          .data(d => [d])
          .join("text")
          .attr("x", 24)
          .attr("y", 9.5)
          .attr("dy", "0.32em")
          .text(d => getChineseLabel(d));
  }

  // Initial chart render
  updateChart();
});
