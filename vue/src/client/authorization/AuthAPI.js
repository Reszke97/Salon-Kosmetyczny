import axios from 'axios';
import store from '../store/index';

const baseURL = 'http://127.0.0.1:8000'
const AUTH_API = axios.create({
    baseURL: baseURL,// Adres do serwera Django
    timeout: 5000,
    headers: {
        Authorization: localStorage.getItem('clientToken')
            ? 'JWT ' + localStorage.getItem('clientToken')
            : null,
            'Content-Type': 'application/json',
            accept: 'application/json',
    },
})

AUTH_API.interceptors.response.use(
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
				alert('Token się wysypał, zaloguj się ponownie')
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
			const clientRefreshToken = localStorage.getItem('clientRefreshToken');

			try{
				if (clientRefreshToken) {
					const tokenParts = JSON.parse(atob(clientRefreshToken.split('.')[1]));
	
					// exp date in clientToken is expressed in seconds, while now() returns milliseconds:
					const now = Math.ceil(Date.now() / 1000);
	
					if (tokenParts.exp > now) {
						return AUTH_API
							.post('/api/v1/token/refresh/', { refresh: localStorage.getItem('clientRefreshToken') })
							.then((response) => {
								store.commit('setToken', {
									access: response.data.access,
									refresh: response.data.refresh
								})

								store.commit('setIsAuthenticated', true);
	
								AUTH_API.defaults.headers['Authorization'] =
									'JWT ' + response.data.access;
								originalRequest.headers['Authorization'] =
									'JWT ' + response.data.access;
									
								return AUTH_API(originalRequest)
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
export {AUTH_API}