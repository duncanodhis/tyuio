/* eslint-disable prettier/prettier */
import React, { useState, useEffect } from 'react';
import {
  CTable,
  CTableHead,
  CTableRow,
  CTableHeaderCell,
  CTableBody,
  CPagination,
} from '@coreui/react';

const Order = () => {
  const [orders, setOrders] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [ordersPerPage] = useState(10); // Adjust as needed

  useEffect(() => {
    // Fetch orders data from the endpoint
    fetch('http://127.0.0.1:5000/api/orders')
      .then((response) => response.json())
      .then((data) => setOrders(data))
      .catch((error) => console.error('Error fetching orders:', error));
  }, []);

  const indexOfLastOrder = currentPage * ordersPerPage;
  const indexOfFirstOrder = indexOfLastOrder - ordersPerPage;
  const currentOrders = orders.slice(indexOfFirstOrder, indexOfLastOrder);

  const paginate = (pageNumber) => setCurrentPage(pageNumber);

  return (
    <div>
      <CTable>
        <CTableHead>
          <CTableRow>
            <CTableHeaderCell>ID</CTableHeaderCell>
            <CTableHeaderCell>Quantity</CTableHeaderCell>
            <CTableHeaderCell>Number of Orders</CTableHeaderCell>
            <CTableHeaderCell>Quantity Unit</CTableHeaderCell>
            <CTableHeaderCell>Total Price</CTableHeaderCell>
            <CTableHeaderCell>Product</CTableHeaderCell>
            <CTableHeaderCell>Customer Telegram ID</CTableHeaderCell>
            <CTableHeaderCell>Transaction Status</CTableHeaderCell>
            <CTableHeaderCell>Treasure ID</CTableHeaderCell>
            <CTableHeaderCell>Created At</CTableHeaderCell>
            {/* Add more header cells as needed */}
          </CTableRow>
        </CTableHead>
        <CTableBody>
          {currentOrders.map((order) => (
            <CTableRow key={order.id}>
              <CTableHeaderCell>{order.id}</CTableHeaderCell>
              <CTableHeaderCell>{order.quantity}</CTableHeaderCell>
              <CTableHeaderCell>{order.number_of_orders}</CTableHeaderCell>
              <CTableHeaderCell>{order.quantity_unit}</CTableHeaderCell>
              <CTableHeaderCell>{order.total_price}</CTableHeaderCell>
              <CTableHeaderCell>{order.product_name ? order.product_name : 'N/A'}</CTableHeaderCell>
              <CTableHeaderCell>{order.customer_telegram_id}</CTableHeaderCell>
              <CTableHeaderCell>{order.payment_status}</CTableHeaderCell>
              <CTableHeaderCell>
                {order.treasure_id ? order.treasure_id : 'N/A'}
              </CTableHeaderCell>
              <CTableHeaderCell>{order.created_at}</CTableHeaderCell>
              {/* Add more data cells as needed */}
            </CTableRow>
          ))}
        </CTableBody>
      </CTable>
      <CPagination
        activePage={currentPage}
        pages={Math.ceil(orders.length / ordersPerPage)}
        onActivePageChange={paginate}
      />
    </div>
  );
};

export default Order;
