<script>
    import HistoryItem from './HistoryItem.svelte'
    let historyItems = [
        {
            src: "https://images.squarespace-cdn.com/content/v1/55be995de4b071c106b3b4c0/1573519454509-3N2QL2Y3QCL2VVNUENKB/Stir+Fried+Tomato+and+Beef+Rice+Bowl+Recipe+-+Eat+Cho+Food",
            description: "Japanese Beef Fried Rice with Tomato",
            prepTime: 25,
            numIngredients: 6,
            ingredients: [
                {
                    name: "Rice",
                    quantity: "500gr",
                }, 
                {
                    name: "Beef",
                    quantity: "200gr",
                }, 
                {
                    name: "Tomato", 
                    quantity: "2"
                }
            ]
        },
        {
            src: "https://whattocooktoday.com/wp-content/uploads/2018/01/IMG_6544.jpg",
            description: "Indonesian Original Nasi Liwet",
            prepTime: 15,
            numIngredients: 4,
            ingredients: [
                {
                    name: "Rice",
                    quantity: "500gr",
                }, 
                {
                    name: "Onion",
                    quantity: "2",
                }, 
            ]
        },
        {
            src: "https://farm8.staticflickr.com/7087/7174177733_6c0af1a0b2_b.jpg",
            description: "Beef Pho",
            prepTime: 60,
            numIngredients: 10,
            ingredients: [
                {
                    name: "Beef",
                    quantity: "200gr",
                }, 
                {
                    name: "Noodles",
                    quantity: "500gr",
                }, 
            ]
        },
    ]
</script>

<div class="mb-4 gap-2">
    {#each historyItems as item, i}
    <HistoryItem {item}/>
    {/each}
</div>