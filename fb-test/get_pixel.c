#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <fcntl.h>
#include <linux/fb.h>
#include <sys/mman.h>
#include <sys/ioctl.h>
#include <linux/kd.h>

int main (int argc, char* argv[])
{

  /* framebuffer file descriptor */
  int fbfd;

  /* tty file descriptor */
  /* if we can't open the tty because it is not writeable then we'll
     just leave it in text mode */
  int ttyfd;

  /* structures for important fb information */
  struct fb_var_screeninfo vinfo;
  struct fb_fix_screeninfo finfo;
  
  /* screen size in bytes */
  /* x * y * bpp / 8 */
  unsigned long int screensize;

  /* Pixel specification 16bpp */
  typedef short pixel_t;

  /* Framebuffer pointer */
  typedef pixel_t* fbp_t;

  fbp_t fbp;

  /* Open framebuffer */
  fbfd = open("/dev/fb0", O_RDWR);
  if(fbfd == -1)
    {
      printf("Error: cannot open framebuffer device");
      exit(1);
    }

  /* Set the tty to graphics mode */
  /* Get fixed screen information */
  if(ioctl(fbfd, FBIOGET_FSCREENINFO, &finfo) == -1)
    {
      printf("Error reading fixed information");
      exit(2);
    }

  /* Get variable screen information */
  if(ioctl(fbfd, FBIOGET_VSCREENINFO, &vinfo) == -1)
    {
      printf("Error reading variable information");
      exit(3);
    }

  printf("%s\n", finfo.id);
  printf("%dx%d, %dbpp\n", vinfo.xres, vinfo.yres, vinfo.bits_per_pixel);
  
  screensize = vinfo.xres * vinfo.yres * vinfo.bits_per_pixel / 8 ;
  printf("%lu bytes\n", screensize);
  
  fbp = (fbp_t)mmap(0, screensize, PROT_READ | PROT_WRITE, MAP_SHARED, fbfd, 0);

  //if ((int)fbp == -1)
  //  {
  //    printf("Error: failed to map framebuffer device to memory\n");
  //    exit(4);
  //  }

  ///* Attempt to open the tty and set it to graphics mode */
  //ttyfd = open("/dev/tty1", O_RDWR);
  //if (ttyfd == -1) {
  //  printf("Error: could not open the tty\n");
  //}else{
  //  ioctl(ttyfd, KDSETMODE, KD_GRAPHICS);
  //}
  //
  //unsigned int i;
  //unsigned int num_pixels = screensize / sizeof ( pixel_t );

  ///* Do your display logic here */
  //for (i=0; i<num_pixels; i++)
  //  {
  //    fbp[i] = i ^ fbp[i];
  //  }

  ///* Unmap the memory and release all the files */
  munmap(fbp, screensize);

  //if (ttyfd != -1)
  //  {
  //    ioctl(ttyfd, KDSETMODE, KD_TEXT);
  //    close(ttyfd);
  //  }

  close(fbfd);

  return 0;
}
