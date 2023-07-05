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
				const originalRequest = error.config;
				if (typeof error.response === 'undefined') {
					alert(
						'A server/network error occurred. ' +
							'Looks like CORS might be the problem. ' +
							'Sorry about this - we will get it fixed shortly.'
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
						store.commit('setIsAuthenticated', false)
						return Promise.reject(error);
					}
					else{
						// window.location.href = 'http://localhost:8080/login';
						alert(error)
						// alert('Token się wysypał, zaloguj się ponownie')
						store.commit('setIsAuthenticated', false)
						return Promise.reject(error);
					}
				}
		
				if (
					error.response.status === 403
				) {
					// window.location.href = 'http://localhost:8080/login';
					alert('Twoje hasło niedawno zostało zmienione, zaloguj się ponownie.')
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
			
							// exp date in token is expressed in seconds, while now() returns milliseconds:
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
								alert('Refresh token is expired', tokenParts.exp, now);
								store.commit('setIsAuthenticated', false);
								// window.location.href = 'http://localhost:8080/login';
							}
						} else {
							store.commit('setIsAuthenticated', false);
							// window.location.href = 'http://localhost:8080/login';
						}
					}catch( error ){
						alert(error)
						// return
					}
				}
				// specific error handling done elsewhere
				return Promise.reject(error);
			}
		);
		newAxiosInstance = axiosInstance;
	})
	return newAxiosInstance
}

export {AUTH_API}