declare global
{
    const TelegramGameProxy: {
        initParams: any,
    }
    // https://core.telegram.org/bots/webapps#initializing-mini-apps
    const Telegram: {
        WebApp: {
            initData: string,
            platform: string,
            colorScheme: "light" | "dark",
        }
    }
}
export { };