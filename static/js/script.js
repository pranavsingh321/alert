document.addEventListener("htmx:afterProcess", function (event) {
  if (event.detail.xhr.responseURL.includes("/chart-data")) {
    const chartData = JSON.parse(event.detail.xhr.responseText);
    const layout = {
      title: "Interactive Time Series Chart",
      xaxis: { title: "Date" },
      yaxis: { title: "Value" },
    };

    // Ensure the chart container exists before rendering
    if (document.getElementById("chart-container")) {
      Plotly.newPlot("chart-container", [chartData], layout);
    } else {
      console.error("Chart container not found.");
    }
  }
});

console.log("after process");
