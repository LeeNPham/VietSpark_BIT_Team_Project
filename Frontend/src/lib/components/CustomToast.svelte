<script lang="ts">
	import { Toast } from 'flowbite-svelte';
	import { CheckCircleSolid, ExclamationCircleSolid } from 'flowbite-svelte-icons';
	import { hideToast, toastStore } from '$lib/stores/alertStore';

	let type = 'success';
	let message: string;
	let show: boolean = false;

	toastStore.subscribe((store) => {
		type = store.type;
		message = store.message;
		show = store.show;
	});

	let timeoutId: ReturnType<typeof setTimeout> | undefined;

	$: if (show) {
		clearTimeout(timeoutId);
		timeoutId = setTimeout(() => {
			hideToast();
		}, 3000);
	}
	const colorMap: Record<typeof type, 'green' | 'red' | 'yellow'> = {
		success: 'green',
		error: 'red',
		warning: 'yellow'
	};

	const iconMap: Record<typeof type, any> = {
		success: CheckCircleSolid,
		error: ExclamationCircleSolid,
		warning: ExclamationCircleSolid
	};

	$: IconComponent = iconMap[type];
	$: toastColor = colorMap[type];

	const handleClose = () => {
		clearTimeout(timeoutId);
		hideToast();
	};
</script>

{#if show}
	<Toast
		color={toastColor}
		dismissable={true}
		class="fixed right-4 top-4 z-50"
		on:close={handleClose}
	>
		<svelte:fragment slot="icon">
			<IconComponent class="h-6 w-6" />
		</svelte:fragment>
		<span class="font-medium">{message}</span>
	</Toast>
{/if}
