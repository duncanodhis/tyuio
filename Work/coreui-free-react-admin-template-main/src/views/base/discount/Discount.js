/* eslint-disable prettier/prettier */
import React, { useState, useEffect } from 'react';
import {
  CForm,
  CFormControlWrapper,
  CFormLabel,
  CFormInput,
  CButton,
  CToast,
  CToastHeader,
  CToastBody,
  CToaster,
  CFormSwitch,
  CFormSelect,
} from '@coreui/react';
import axios from 'axios';

function Discount() {
  const [selectedProduct, setSelectedProduct] = useState(''); // Store the selected product ID
  const [numberOfPurchases, setNumberOfPurchases] = useState(0);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [amountOfPurchases, setAmountOfPurchases] = useState(0);
  const [currency, setCurrency] = useState('Euro');
  const [discountPercentage, setDiscountPercentage] = useState(0);
  const [isDiscountEnabled, setIsDiscountEnabled] = useState(false);
  const [productOptions, setProductOptions] = useState([]); // Store product options

  const [toast, addToast] = useState(null);
  const toaster = React.createRef();

  useEffect(() => {
    // Fetch product options from your API endpoint
    axios.get('http://127.0.0.1:5000/api/products').then((response) => {
      // Assuming the API response is an array of objects with 'id' and 'name' properties
      setProductOptions(response.data);
    });
  }, []);

  useEffect(() => {
    if (isDiscountEnabled) {
      const currentTime = new Date();
      const startDateTime = new Date(startDate);
      const endDateTime = new Date(endDate);

      const totalDuration = endDateTime - startDateTime;
      const elapsedTime = currentTime - startDateTime;

      const progressPercentage = (elapsedTime / totalDuration) * 100;

      if (progressPercentage >= 0 && progressPercentage < 100) {
        const beginToast = (
          <CToast key="beginToast">
            <CToastHeader>Discount Started</CToastHeader>
            <CToastBody>The discount has started!</CToastBody>
          </CToast>
        );
        addToast(beginToast);
      }

      if (progressPercentage >= 100) {
        const endToast = (
          <CToast key="endToast">
            <CToastHeader>Discount Ended</CToastHeader>
            <CToastBody>The discount has ended!</CToastBody>
          </CToast>
        );
        addToast(endToast);
      }
    }
  }, [startDate, endDate, isDiscountEnabled]);

  const handleApplyDiscount = () => {
    const discountData = {
      productId: selectedProduct, // Send the selected product ID
      productName: productOptions.find((product) => product.id === selectedProduct)?.name || '', // Send the selected product name
      numberOfPurchases,
      startDate,
      endDate,
      amountOfPurchases,
      currency,
      discountPercentage,
      isDiscountEnabled,
    };

    axios
      .post('http://127.0.0.1:5000/api/discount', discountData)
      .then((response) => {
        console.log('Discount applied successfully:', response.data);
        const successToast = (
          <CToast key="successToast">
            <CToastHeader>Discount Set</CToastHeader>
            <CToastBody>Discount applied successfully!</CToastBody>
          </CToast>
        );
        addToast(successToast);
      })
      .catch((error) => {
        console.error('Error applying discount:', error);
        const errorToast = (
          <CToast key="errorToast">
            <CToastHeader>Error</CToastHeader>
            <CToastBody>Error applying discount!</CToastBody>
          </CToast>
        );
        addToast(errorToast);
      });
  };

  return (
    <>
      <CForm>
        <CFormControlWrapper>
          <CFormLabel>Product Name</CFormLabel>
          <CFormSelect
            custom
            value={selectedProduct}
            onChange={(e) => setSelectedProduct(e.target.value)}
          >
            <option value="">Select a product</option>
            {productOptions.map((product) => (
              <option key={product.id} value={product.id}>
                {product.name}
              </option>
            ))}
          </CFormSelect>
        </CFormControlWrapper>
        <CFormControlWrapper>
          <CFormLabel>Number of Purchases</CFormLabel>
          <CFormInput
            type="number"
            value={numberOfPurchases}
            onChange={(e) => setNumberOfPurchases(e.target.value)}
          />
        </CFormControlWrapper>
        <CFormControlWrapper>
          <CFormLabel>Start Date</CFormLabel>
          <CFormInput
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
          />
        </CFormControlWrapper>
        <CFormControlWrapper>
          <CFormLabel>End Date</CFormLabel>
          <CFormInput
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
          />
        </CFormControlWrapper>
        <CFormControlWrapper>
          <CFormLabel>
            Amount of Purchases
            <select
              value={currency}
              onChange={(e) => setCurrency(e.target.value)}
            >
              <option value="Euro">Euro</option>
              <option value="GEL">GEL</option>
            </select>
          </CFormLabel>
          <CFormInput
            type="number"
            value={amountOfPurchases}
            onChange={(e) => setAmountOfPurchases(e.target.value)}
          />
        </CFormControlWrapper>
        <CFormControlWrapper>
          <CFormLabel>Discount Percentage</CFormLabel>
          <CFormInput
            type="number"
            value={discountPercentage}
            onChange={(e) => setDiscountPercentage(e.target.value)}
          />
        </CFormControlWrapper>
        <CFormControlWrapper>
          <CFormLabel>Enable Discount</CFormLabel>
          <CFormSwitch
            id="enableDiscountSwitch"
            onChange={() => setIsDiscountEnabled(!isDiscountEnabled)}
            defaultChecked={isDiscountEnabled}
          />
        </CFormControlWrapper>
      </CForm>

      <CButton
        color="primary"
        onClick={handleApplyDiscount}
        disabled={isDiscountEnabled}
      >
        Apply Discount
      </CButton>

      <CToaster ref={toaster} push={toast} placement="top-end" />
    </>
  );
}

export default Discount;
