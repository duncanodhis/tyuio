/* eslint-disable prettier/prettier */
/* eslint-disable no-restricted-globals */
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  CButton,
  CModal,
  CModalHeader,
  CModalTitle,
  CModalBody,
  CModalFooter,
  CTooltip,
  CForm,
  CCol,
  CFormInput,
  CFormSelect,
  CToast,
  CToastBody,
  CToastHeader,
} from '@coreui/react';

const AddTask = () => {
  const [visible, setVisible] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState('');
  const [areaOfDistribution, setAreaOfDistribution] = useState('');
  const [numOfItems, setNumOfItems] = useState('');
  const [costOfItem, setCostOfItem] = useState('');
  const [weightOfItem, setWeightOfItem] = useState('');
  const [courierCommission, setCourierCommission] = useState('');
  const [showToast, setShowToast] = useState(false);
  const [products, setProducts] = useState([]);
  const[ItemWeightMeasurement,setItemWeightMeasurement] = useState([])
  const[commissionCurrency,setCommissionCurrency] = useState([])
  const [couriers, setCouriers] = useState([]);
  const [selectedCourier,setSelectedCourier]=useState([])
  const [taskName, setTaskName] = useState('');
  const [numOfTreasures, setNumOfTreasures] = useState('');

   useEffect(() => {
    fetch('http://127.0.0.1:5000/api/products')
      .then((response) => response.json())
      .then((data) => {
        setProducts(data)
      })
      .catch((error) => console.error('Error fetching products :', error))
  }, [])
  
  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/couriers')
      .then((response) => response.json())
      .then((data) => {
        setCouriers(data)
      })
      .catch((error) => console.error('Error fetching couriers :', error))
  }, [])
  const handleAddTasks = async (event) => { // Add 'event' as a parameter here
    event.preventDefault();
    event.stopPropagation();
    const form = event.currentTarget;
    if (form.checkValidity() === false) {
      // Handle form validation errors if needed
      return;
    } else {
      const taskData = {
        taskName: taskName,
        number_of_treasures: numOfTreasures,
        courier:selectedCourier,
        product: selectedProduct,
        address: areaOfDistribution,
        number_of_items: numOfItems,
        cost_of_item: costOfItem,
        weight_of_item: weightOfItem,
        item_weight_measurement: ItemWeightMeasurement,
        courier_commission: courierCommission,
        commission_currency: commissionCurrency,
      };
      console.log('Product data to be sent:', taskData);

      try {
        const response = await axios.post('http://127.0.0.1:5000/api/tasks', taskData, {
          headers: {
            'Content-Type': 'application/json',
          },
        });
        console.log('Task data submitted successfully:', response.data);
        // Optionally, you can reset the form fields after successful submission
        setSelectedProduct('');
        setSelectedCourier('');
        setAreaOfDistribution('');
        setNumOfItems('');
        setCostOfItem('');
        setWeightOfItem('');
        setCourierCommission('');
        setShowToast(true);
        setItemWeightMeasurement('');
        setCommissionCurrency('GEL');
        setVisible(false); // Close the modal or hide the form after successful submission
      } catch (error) {
        // Handle any errors that occurred during the API call
        console.error('Error submitting product data:', error);
      }
    }
  };


  return (
    <>
      <CTooltip
        content="Make sure to create 🌱packaging,📌Addresses on the navigation bar 👆 first before adding product"
        placement="right"
      >
        <CButton onClick={() => setVisible(!visible)}>Add Tasks</CButton>
      </CTooltip>

      <CModal alignment="center" size="lg" visible={visible} onClose={() => setVisible(false)}>
        <CModalHeader>
          <CModalTitle>Add Tasks</CModalTitle>
        </CModalHeader>
        <CModalBody>
              <CCol md={6}>
              <CFormInput
                id="taskName"
                label="Task Name"
                value={taskName}
                onChange={(e) => setTaskName(e.target.value)}
              />
            </CCol>

          <CForm className="row g-3">
              <CCol md={6}>
            <CFormSelect
              id="courier"
              label="Courier"
              value={selectedCourier}
              onChange={(e) => setSelectedCourier(e.target.value)}
            >
              <option value="">Choose...</option>
              {couriers.map((courier) => (
                <option key={courier.id} value={courier.id}>
                  {courier.name}
                </option>
              ))}
            </CFormSelect>
          </CCol>

            <CCol md={6}>
            <CFormSelect
              id="product"
              label="Product"
              value={selectedProduct}
              onChange={(e) => setSelectedProduct(e.target.value)}
            >
              <option>Choose...</option>
              {products.map((product) => (
                <option key={product.id} value={product.id}
                style={{ paddingLeft: '20px' }} 
                >
                  Product: {product.name}
                  <br />
                  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; District of Sale: {product.district}
                </option>
              ))}
            </CFormSelect>
            </CCol>
            <CCol md={6}>
              <CFormInput
                id="areaOfDistribution"
                label="Area of Distribution"
                value={areaOfDistribution}
                onChange={(e) => setAreaOfDistribution(e.target.value)}
              />
            </CCol>
            <CCol md={6}>
              <CFormInput
                id="numOfItems"
                label="Number of Items in Bag"
                value={numOfItems}
                onChange={(e) => setNumOfItems(e.target.value)}
              />
            </CCol>
            <CCol md={6}>
              <CFormInput
                id="costOfItem"
                label="Cost of Each Item"
                value={costOfItem}
                onChange={(e) => setCostOfItem(e.target.value)}
              />
            </CCol>
            <CCol md={6}>
            <CFormSelect
              id="weight-measurement"
              label="weight"
              value={ItemWeightMeasurement}
              onChange={(e) => setItemWeightMeasurement(e.target.value)}
            > <option value="">Choose...</option>
              <option value="g">grams</option>
              <option value="mg">milligrams</option>
              <option value="pieces">pieces</option>
            </CFormSelect>
            </CCol>
            <CCol md={6}>
              <CFormInput
                id="weightOfItem"
                label="Weight of Each Item"
                value={weightOfItem}
                onChange={(e) => setWeightOfItem(e.target.value)}
              />
            </CCol>
            <CCol md={6}>
            <CFormInput
              id="numOfTreasures"
              label="Number of Treasures"
              value={numOfTreasures}
              onChange={(e) => setNumOfTreasures(e.target.value)}
            />
          </CCol>
            <CCol md={6}>
              <CFormInput
                id="courierCommission"
                label="Courier's Commission"
                value={courierCommission}
                onChange={(e) => setCourierCommission(e.target.value)}
              />
            </CCol>
            <CCol md={6}>
              <CFormSelect
                id="commission-currency"
                label="Commission Currency"
                value={commissionCurrency}
                onChange={(e) => setCommissionCurrency(e.target.value)}
              >
                <option value="">Choose</option>
                <option value="GEL">GEL</option>
                <option value="EUR">EUR</option>              
              </CFormSelect>
            </CCol>
          </CForm>
        </CModalBody>
        <CModalFooter>
          <CButton color="secondary" onClick={() => setVisible(false)}>
            Close
          </CButton>
          <CTooltip
            content="Stock price is the same as package price, so you have to input the selling price for the clients to see"
            placement="right"
          >
            <CButton color="primary" onClick={handleAddTasks}>
              Save changes
            </CButton>
          </CTooltip>
        </CModalFooter>
      </CModal>

      {/* Toast message */}
      <CToast position="top-end">
        <CToast show={showToast} autohide={3000} onDismiss={() => setShowToast(false)}>
          <CToastHeader closeButton>Saved Successfully</CToastHeader>
          <CToastBody>Your changes have been saved successfully.</CToastBody>
        </CToast>
      </CToast>
    </>
  );
};

export default AddTask;
