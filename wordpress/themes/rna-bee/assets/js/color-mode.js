(() => {
	const storageKey = 'rna-bee-color-mode';

	const getStoredMode = () => {
		const value = localStorage.getItem(storageKey);

		return value === 'light' || value === 'dark'
			? value
			: null;
	};

	const getPreferredMode = () => {
		return window.matchMedia('(prefers-color-scheme: dark)').matches
			? 'dark'
			: 'light';
	};

	const applyMode = (mode) => {
		document.documentElement.dataset.colorMode = mode;

		document
			.querySelectorAll('[data-rna-color-mode-toggle]')
			.forEach((button) => {
				const nextMode = mode === 'dark' ? 'light' : 'dark';

				button.setAttribute(
					'aria-label',
					`Switch to ${nextMode} mode`
				);

				button.setAttribute(
					'title',
					`Switch to ${nextMode} mode`
				);

				button.textContent = mode === 'dark'
					? 'Light'
					: 'Dark';
			});
	};

	const initialize = () => {
		applyMode(getStoredMode() ?? getPreferredMode());

		document
			.querySelectorAll('[data-rna-color-mode-toggle]')
			.forEach((button) => {
				button.addEventListener('click', () => {
					const current =
						document.documentElement.dataset.colorMode;

					const next =
						current === 'dark' ? 'light' : 'dark';

					localStorage.setItem(storageKey, next);
					applyMode(next);
				});
			});

		window
			.matchMedia('(prefers-color-scheme: dark)')
			.addEventListener('change', (event) => {
				if (getStoredMode() === null) {
					applyMode(event.matches ? 'dark' : 'light');
				}
			});
	};

	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', initialize);
	} else {
		initialize();
	}
})();