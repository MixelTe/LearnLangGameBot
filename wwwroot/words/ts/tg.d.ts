declare global
{
    const TelegramGameProxy: {
        initParams: any,
    }
    const Telegram: {
        WebApp: {
            initData: string,
            platform: string,
            colorScheme: "light" | "dark",
        }
    }
}
export { };