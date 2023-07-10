import axios from 'axios';
import store from '../store/index';

const baseURL = 'http://127.0.0.1:8000'


const delay = (time, callBack) => {
	return new Promise ((resolve) => {
		setTimeout(resolve.bind(null, callBack), time)
	})
}

Promise.prototype.delay = function(time){
	return this.then((method) => {
		return delay(time, method)
	})
}

const AUTH_API = async () => {
	let originalRequest = null;
	let newAxiosInstance = null;
	await Promise.resolve()
	.delay(100)
	.then(() => {
		const axiosInstance = axios.create({
			baseURL: baseURL,// Adres do serwera Django
			timeout: 5000,
			headers: {
				Authorization: localStorage.getItem('employeeToken')
					? 'JWT ' + localStorage.getItem('employeeToken')
					: null,
					'Content-Type': 'application/json',
					accept: 'application/json',
			},
		})
	
		axiosInstance.interceptors.response.use(
			(response) => {
				return response;
			},
			async function (error) {
				if (!originalRequest){
					originalRequest = error.config;
				}
				if (typeof error.response === 'undefined') {
					alert(
						"Wystąpiły problemy z serwerem. Naprawa w trakcie."
					);
					store.commit('setIsAuthenticated', false)
					return Promise.reject(error);
				}
		
				if(
					(
						error.response.status === 401 && (
							error.response.data.detail === 'Token contained no recognizable user identification' 
							||  originalRequest.url === '/api/v1/token/verify/'
						)
					)
					|| error.response.status === 400
				){
					console.log('a')
					alert('Niepoprawny token')
					store.commit('setIsAuthenticated', false)
					return Promise.reject(error);
				}
		
				if (
					error.response.status === 401 &&
					originalRequest.url === '/api/v1/token/refresh/'
				) {
					if(error.response.data.detail === 'Twoje Hasło zostało przed chwilą zmienione, proszę zalogować się ponownie.'){
						alert('Twoje hasło niedawno zostało zmienione, zaloguj się ponownie.')
						localStorage.removeItem("employeeToken");
						localStorage.removeItem("employeeRefreshToken");
						store.commit('setIsAuthenticated', false)
						return Promise.reject(error);
					}
					else{
						alert(error)
						store.commit('setIsAuthenticated', false)
						return Promise.reject(error);
					}
				}
		
				if (
					error.response.status === 403
				) {
					alert('Twoje hasło niedawno zostało zmienione, zaloguj się ponownie.')
					localStorage.removeItem("employeeToken");
					localStorage.removeItem("employeeRefreshToken");
					store.commit('setIsAuthenticated', false)
					return Promise.reject(error);
				}
		
				if (
					(error.response.data.code === 'token_not_valid' || error.response.data.detail === 'Authentication credentials were not provided.') &&
					originalRequest.url !== '/api/v1/token/verify/' &&
					error.response.status === 401 &&
					error.response.statusText === 'Unauthorized'
				) {
					const employeeRefreshToken = localStorage.getItem('employeeRefreshToken');
		
					try{
						if (employeeRefreshToken) {
							const tokenParts = JSON.parse(atob(employeeRefreshToken.split('.')[1]));
							const now = Math.ceil(Date.now() / 1000);
			
							if (tokenParts.exp > now) {
								return axiosInstance
									.post('/api/v1/token/refresh/', { refresh: localStorage.getItem('employeeRefreshToken') })
									.then((response) => {
										store.commit('setToken', {
											access: response.data.access,
											refresh: response.data.refresh
										})
		
										store.commit('setIsAuthenticated', true);
			
										axiosInstance.defaults.headers['Authorization'] =
											'JWT ' + response.data.access;
										originalRequest.headers['Authorization'] =
											'JWT ' + response.data.access;
											
										return axiosInstance(originalRequest)
									})
									.catch((err) => {
										store.commit('setIsAuthenticated', false);
										return Promise.reject(error);
									});
							} else {
								alert('Token wygasł', tokenParts.exp, now);
								store.commit('setIsAuthenticated', false);
							}
						} else {
							store.commit('setIsAuthenticated', false);
						}
					}catch( error ){
						alert("Nieprawidłowy token. Zaloguj się ponownie.")
					}
				}
				return Promise.reject(error);
			}
		);
		newAxiosInstance = axiosInstance;
	})
	return newAxiosInstance
}

export {AUTH_API}