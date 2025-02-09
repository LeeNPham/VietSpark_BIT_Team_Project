export const customStyles = {
    navBar: "flex flex-wrap items-center justify-between rounded-full py-4",
    heading: "pb-4 sm:pb-4 md:pb-9 lg:pb-9 font-sans text-lg sm:text-lg md:text-2xl lg:text-5xl font-bold  text-black",
    categoryBtn: " p-4  m-2 text-xs  text-black outline sm:text-xs md:text-2xl lg:text-3xl  rounded-2xl bg-primary-green hover:bg-secondary-blue outline-secondary-green",
    category: "flex justify-center pb-4 font-sans text-lg font-bold text-black sm:pb-4 sm:text-lg md:pb-9 md:text-2xl lg:pb-9 lg:text-5xl",
    aTag: "text-2xl text-teal-600",
};
// Function to add the alt attribute to all images
export function addAltTextToImages(defaultAltText: string = "Image"): void {
    const imgs = document.getElementsByTagName("img");
    for (let img of imgs) {
        if (!img.hasAttribute("alt")) {
            img.setAttribute("alt", defaultAltText);
        }
    }
}

export interface ImageAttributes {
    src: string;
    alt: string;
    class: string;
}