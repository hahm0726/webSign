import {  axiosService } from "/src/api/config";

/*billData의 인수증 데이터 생성 요청*/
function createBill (billData){
    
    const url = '/bills/bill/';
    return axiosService.post(url,billData);
}

/*billId의 인수증 데이터 정보 요청*/
function getBill (billId){
    const url = `/bills/bill/${billId}/`;
    return axiosService.get(url);
}

/*billId의 인수증 데이터 billData로 수정 요청*/
function updateBill (billId,billData){
    const url = `/bills/bill/${billId}/`;
    return axiosService.patch(url,billData);
}

/*billId 인수증 데이터 삭제 요청*/
function deleteBill (billId){
    const url = `/bills/bill/${billId}/`;
    return axiosService.delete(url);
}

/*다중 인수증 데이터 정보 요청*/
function getBillAll (){
    const url = '/bills/bill/';
    return axiosService.get(url);
}

/*다중 인수증 데이터 생성 요청*/
function createBillList (billListData){
    const url = '/bills/bill-list/';
    return axiosService.post(url,billListData);
}
/*다중 인수증 데이터 수정 요청(검증 요망)*/
function updateBillList (billListData){
    const url = '/bills/bill-list/';
    return axiosService.patch(url,billListData);
}
/*다중 인수증 데이터 삭제 요청(검증 요망)*/
function deleteBillList (billListData){
    const url = '/bills/bill-list/';
    return axiosService.delete(url,billListData);
}

export {
    createBill,
    getBill,
    updateBill,
    deleteBill,
    getBillAll,
    createBillList,
    updateBillList,
    deleteBillList,
}
