/*---------------------------------------------------------------------------------

    Copyright (C) 2012-2014
        Alekmaul


    This software is provided 'as-is', without any express or implied
    warranty.  In no event will the authors be held liable for any
    damages arising from the use of this software.

    Permission is granted to anyone to use this software for any
    purpose, including commercial applications, and to alter it and
    redistribute it freely, subject to the following restrictions:

    1.	The origin of this software must not be misrepresented; you
        must not claim that you wrote the original software. If you use
        this software in a product, an acknowledgment in the product
        documentation would be appreciated but is not required.

    2.	Altered source versions must be plainly marked as such, and
        must not be misrepresented as being the original software.

    3.	This notice may not be removed or altered from any source
        distribution.

---------------------------------------------------------------------------------*/
/*! \file lzss.h
\brief Wrapper functions for lzss decoding

*/
#ifndef SNES_LZSS_INCLUDE
#define SNES_LZSS_INCLUDE

#include "snestypes.h"

/*! \brief Decompress Lzss data to VRAM
    \param source the source to decompress from
    \param address vram address to decompress
    \param size the size in bytes of the data to decompress.
*/
void LzssDecodeVram(u8 *source, u16 address, u16 size);

#endif // SNES_LZSS_INCLUDE
