describe("Fill Minder Fields", () => {
    beforeEach(() => {
      // Mock sessionStorage
      const sessionData = {
        minderId: '123',
        minderUser: 'john_doe',
        minderName: 'John Doe',
        minderPhotoUrl: 'placeholder',
        minderAvailability: 'Mon - Fri',
      };
      Object.defineProperty(window, 'sessionStorage', {
        value: {
          getItem: jest.fn((key) => sessionData[key]),
        },
      });
  
      // Set up the DOM elements
      document.body.innerHTML = `
        <select id="id_minder"></select>
        <input id="id_minder_name" />
        <img id="minder_photo_booking" />
        <p id="minder-name-booking"></p>
        <p id="minder-availability-booking"></p>
        <button class="reselect-minder-btn"></button>
      `;
  
      // Import and execute the code
      require('../../static/js/fill_minder_fields.js');
    });
  
    test("should fill in the minder fields", () => {
      expect(document.getElementById('id_minder').value).toBe('123');
      expect(document.getElementById('id_minder_name').value).toBe('John Doe');
      expect(document.getElementById('minder-name-booking').textContent).toBe('You are booking with John Doe');
      expect(document.getElementById('minder-availability-booking').textContent).toBe('Please note the minder usual availability. John Doe is usually available: Mon - Fri');
      expect(document.getElementById('minder_photo_booking').src).toBe('https://res.cloudinary.com/dls3mbdix/image/upload/v1690889814/static/img/profile-placeholder_hgqisr.webp');
    });
    
});
    
  