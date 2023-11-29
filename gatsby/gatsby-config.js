module.exports = {
  pathPrefix: `/`,
  siteMetadata: {
    title: 'kyle harrington\'s cold-storage album for cryoET',
    subtitle: 'album solutions for processing/viz/ML of cryoET data',
    catalog_url: 'https://github.com/kephale/cold-storage',
    menuLinks:[
      {
         name:'Catalog',
         link:'/catalog'
      },
      {
         name:'About',
         link:'/about'
      },
    ]
  },
  plugins: [{ resolve: `gatsby-theme-album`, options: {} }],
}
