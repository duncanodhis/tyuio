import React from 'react'
import {
  CCard,
  CCol,
  CRow,
  CAccordion,
  CAccordionItem,
  CAccordionHeader,
  CAccordionBody,
} from '@coreui/react'
import SalesChart from './SalesChart'
import LineCharts from './LineCharts'
import DoughnutChart from './DoughnutChart'
import PolarChart from './PolarChart'
import PieChart from './PieChart'
const Charts = () => {
  return (
    <CRow>
      <CCol xs={12}>
        <CAccordion activeItemKey={2}>
          <CAccordionItem itemKey={1}>
            <CAccordionHeader>Sales Over a Year - Bar Chart</CAccordionHeader>
            <CAccordionBody>
              <div className="p-4">
                <strong className="text-primary">
                  Visualize the sales performance of your products over the course of a year.
                </strong>
                <p className="mt-3">
                  The SalesChart component is designed to visually represent and display sales data
                  over time in a user-friendly manner. For an end user reading the chart, here
                  &apos;s a description of what the SalesChart does:
                </p>

                {/* ... Rest of the text ... */}

                <p className="mt-3">
                  <strong>Usage:</strong> This Sales Chart is a valuable tool for businesses and
                  individuals who want to visualize their sales performance over time, make
                  data-driven decisions, and track sales trends. It provides a clear and accessible
                  way to understand sales data at a glance.
                </p>
              </div>
            </CAccordionBody>
          </CAccordionItem>

          <CAccordionItem itemKey={2}>
            <CAccordionHeader>Customer Segmentation Pie Chart</CAccordionHeader>
            <CAccordionBody>
              <strong>What the Pie Chart Shows:</strong>
              <p>
                The pie chart illustrates how customers are segmented based on their purchases of
                different products.
              </p>

              <strong>How It&apos;s Calculated:</strong>
              <ol>
                <li>
                  <strong>Grouping by Product:</strong> First, it groups customers by the product
                  they purchased.
                </li>
                <li>
                  <strong>Counting Orders:</strong> It then counts the number of orders made for
                  each product. This count represents how many times each product has been ordered
                  by customers.
                </li>
              </ol>

              <strong>Why It&apos;s Helpful:</strong>
              <ul>
                <li>
                  <strong>Product Popularity:</strong> The chart helps understand which products are
                  more popular among customers. Products with larger segments in the pie chart have
                  been ordered more frequently.
                </li>
                <li>
                  <strong>Segmentation:</strong> It segments customers based on their product
                  choices. You can see which products attract different customer groups.
                </li>
                <li>
                  <strong>Data-Driven Decisions:</strong> This information can guide business
                  decisions, such as optimizing marketing strategies for specific products or
                  tailoring product offerings to different customer segments.
                </li>
                <li>
                  <strong>Visual Clarity:</strong> The pie chart provides a clear and visual
                  representation of customer preferences, making it easier to identify trends and
                  patterns.
                </li>
                <li>
                  <strong>Business Insights:</strong> By analyzing this chart, you can gain insights
                  into customer behavior and product performance, which can be valuable for making
                  informed business choices.
                </li>
              </ul>
            </CAccordionBody>
          </CAccordionItem>

          <CAccordionItem itemKey={3}>
            <CAccordionHeader>Data Retrieval and Visualization - Line Chart</CAccordionHeader>
            <CAccordionBody>
              <p>
                This component serves as the backbone for analyzing essential business metrics. It
                diligently retrieves data from your clients, each representing a crucial aspect of
                your business:
              </p>
              <ul>
                <li>
                  Sales Data: Reflects the total sales over specific time periods, typically in
                  months or years.
                </li>
                <li>
                  Retention Rates: Measures the effectiveness of customer retention strategies by
                  showcasing the percentage of customers who continue to engage with your business
                  over time.
                </li>
                <li>
                  Return Rates: Provides insights into customer satisfaction by displaying the
                  percentage of orders that result in returns.
                </li>
                <li>
                  Average Order Value: Offers valuable information about customer spending habits by
                  representing the average value of each customer&apos;s order.
                </li>
              </ul>
              <p>
                Once the data is retrieved, this component brings it to life through a dynamic line
                chart. Line charts are adept at visualizing trends and patterns over time, making
                them an ideal choice for business analysis.
              </p>
              <p>
                The key metrics are plotted on the chart:
                <ul>
                  <li>
                    <strong>Sales:</strong> Track changes in total revenue over time, helping you
                    assess business growth.
                  </li>
                  <li>
                    <strong>Retention Rate:</strong> Gauge the strength of customer loyalty by
                    monitoring the percentage of returning customers.
                  </li>
                  <li>
                    <strong>Return Rate:</strong> Analyze customer satisfaction by keeping an eye on
                    the percentage of returned orders.
                  </li>
                  <li>
                    <strong>Average Order Value:</strong> Understand customer spending behavior by
                    observing changes in average order values.
                  </li>
                </ul>
              </p>
              <p>
                The x-axis of the chart represents time, and data is segmented based on specified
                time periods, often in months or years. This segmentation allows for a granular
                analysis of these key metrics over different intervals.
              </p>
              <p>
                You can interpret trends and patterns from this chart to make informed decisions.
                For instance:
                <ul>
                  <li>
                    Rising sales suggest business growth, prompting consideration of pricing
                    strategies and expansion opportunities.
                  </li>
                  <li>
                    Consistently high retention rates indicate strong customer loyalty, potentially
                    leading to focused marketing campaigns.
                  </li>
                  <li>
                    Fluctuations in return rates may signal product quality or customer satisfaction
                    issues, necessitating corrective actions.
                  </li>
                  <li>
                    Changes in average order value provide insights into shifts in customer
                    behavior, guiding marketing and sales tactics.
                  </li>
                </ul>
              </p>
              <p>
                It&apos;s worth noting that this component handles cases where data may be
                incomplete or missing for some metrics or time periods, ensuring that the chart only
                displays meaningful and complete information.
              </p>
            </CAccordionBody>
          </CAccordionItem>

          <CAccordionItem itemKey={4}>
            <CAccordionHeader>Revenue Distribution by Product - Doughnut Chart</CAccordionHeader>
            <CAccordionBody>
              <p>
                This component provides a visual representation of how your business revenue is
                distributed among different products. It&apos;s like slicing a delicious doughnut
                into segments to see which flavors are the most popular.
              </p>
              <p>
                The data for this chart is fetched from an API endpoint, ensuring that the chart is
                always up-to-date with your latest revenue data.
              </p>
              <p>In the chart:</p>
              <ul>
                <li>Each segment of the doughnut represents a product that your business sells.</li>
                <li>
                  The size of each segment is proportional to the revenue generated by that product.
                </li>
                <li>
                  The colors of the segments are randomly assigned to make the chart visually
                  appealing.
                </li>
              </ul>
              <p>
                The chart&apos;s title,&quot;Revenue Distribution by Product,&quot; tells you what
                it&apos;s all about. It helps answer questions like:
              </p>
              <ul>
                <li>&quot;Which products are contributing the most to our revenue?&quot;</li>
                <li>
                  &quot;Are there any products that need more attention in terms of marketing or
                  sales efforts?&quot;
                </li>
                <li>&quot;How diverse is our revenue stream among different products?&quot;</li>
              </ul>
              <p>
                The legend on the right side of the chart provides labels for each product, and the
                color of the labels matches the color of the corresponding doughnut segment.
              </p>
              <p>
                This chart is an invaluable tool for business analysts and decision-makers, as it
                allows you to quickly grasp the revenue distribution landscape, make informed
                decisions, and fine-tune your business strategy.
              </p>
            </CAccordionBody>
          </CAccordionItem>
          <CAccordionItem itemKey={5}>
            <CAccordionHeader>Sales by Category - Polar Area Chart</CAccordionHeader>
            <CAccordionBody>
              <p>
                Imagine this chart as a colorful radar showing how your business sales are
                distributed across different categories of products or services. It&apos;s like
                looking at a radar screen, but instead of weather patterns, you&apos;re tracking
                your sales performance.
              </p>
              <p>
                This chart is created using data fetched from an API endpoint, ensuring that you
                always have the latest sales data represented visually.
              </p>
              <p>Here&apos;s what you&apos;ll find in the chart:</p>
              <ul>
                <li>
                  Different categories of products or services are displayed around the circle.
                </li>
                <li>
                  Each category is represented by a colorful segment, and the size of the segment
                  corresponds to the total sales in that category.
                </li>
                <li>
                  The colors are randomly assigned to make the chart visually appealing and easy to
                  distinguish.
                </li>
              </ul>
              <p>
                The chart&apos;s title, &quot;Sales by Category,&quot; tells you exactly what
                it&apos;s showing. It helps answer questions like:
              </p>
              <ul>
                <li>
                  &quot;Which product categories are performing the best in terms of sales?&quot;
                </li>
                <li>
                  &quot;Are there any categories that need more attention or marketing
                  efforts?&quot;
                </li>
                <li>
                  &quot;How evenly distributed are our sales across different categories?&quot;
                </li>
              </ul>
              <p>
                This chart is a valuable tool for business analysts and decision-makers, as it
                provides an at-a-glance overview of your sales landscape. It helps you identify
                trends, make informed decisions, and adjust your business strategy as needed.
              </p>
            </CAccordionBody>
          </CAccordionItem>
        </CAccordion>
      </CCol>
      <SalesChart />
      <CCol xs={6}>
        <LineCharts />
      </CCol>
      <CCol xs={6}>
        <DoughnutChart />
      </CCol>
      <CCol xs={6}>
        <PieChart />
      </CCol>
      <CCol xs={6}>
        <CCard className="mb-4">
          <PolarChart />
        </CCard>
      </CCol>
    </CRow>
  )
}

export default Charts
